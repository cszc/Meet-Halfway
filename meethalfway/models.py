from django.db import models
import requests
import json
import time
import re
import googlemaps
import csv
from random_words import RandomWords

class Address(models.Model):
    street = models.CharField(max_length = 64)
    city = models.CharField(max_length = 64)
    state = models.CharField(max_length = 2)
    zip_code = models.CharField(max_length = 5)
    def __str__(self):
        return "%s %s %s %s" % (self.street, self.city, self.state, self.zip_code)

class Participant(models.Model):
    TRANSIT_TYPES = (
        ("walking", "Walking"),
        ("transit", "Public Transit"),
        ("driving", "Driving"),
        ("bicycling", "Bicycling")
        )
    starting_location = models.ForeignKey(Address, null=True, blank = True)
    transit_mode = models.CharField(max_length = 70, choices = TRANSIT_TYPES)

    # def __str__(self):
    #     return "%s %s" % (self.starting_location, self.transit_mode)

    def get_id(self):
        return self.id

class Destination(models.Model):
    address = models.CharField(max_length = 100, null=True, blank = True)
    a_time = models.CharField(max_length = 3, null=True, blank = True)
    b_time = models.CharField(max_length = 3, null=True, blank = True)
    latlng = models.CharField(max_length = 64, null=True, blank = True)
    name = models.CharField(max_length = 64, null=True, blank = True)
    place_id = models.CharField(max_length = 64, null=True, blank = True)
    score = models.CharField(max_length = 3, null=True, blank = True)
    avg_time = models.CharField(max_length = 3, null=True, blank = True)

class Meeting(models.Model):
    BUSINESS_TYPES = (
        ("cafe", "Cafe"),
        ("bar", "Bar"),
        ("restaurant", "Restaurant"),
        ("museum", "Museum"),
        ("park", "Park")
        )
    participant_one = models.ForeignKey(
        Participant, related_name = 'participant_one', null = True, blank =  True)
    participant_two = models.ForeignKey(
        Participant, related_name = 'participant_two', null = True, blank = True)
    business_type = models.CharField(
        max_length=64, null=True, blank=True, choices = BUSINESS_TYPES)
    trip_id = models.CharField(
        max_length = 100, null=True, blank = True)
    destinations = models.ManyToManyField(
        Destination, blank = True)
    share_location = models.BooleanField(default = False)
    
    def set_participant_two(self, participant):
        self.participant_two = participant

    def get_id(self):
        return self.id

    def random_words(self):
        #for url creation
        rw =  RandomWords()
        w1 = rw.random_word()
        w2 = rw.random_word()
        w3 = rw.random_word()
        return w1 + "-" + w2 + "-" + w3

    def get_destinations(self):
        with open('apikeys.txt', 'r') as f:
            apikey = f.readline().strip()

        gmaps = googlemaps.Client(key=apikey)
        address1 = str(self.participant_one.starting_location)
        address2 = str(self.participant_two.starting_location)

        mode1 = self.participant_one.transit_mode
        mode2 = self.participant_two.transit_mode

        #Step 1: Get potential destinations based on midpoint for each participant
        #returns pseudo json/dicts of dicts
        directions_a = self.get_directions(gmaps, address1, address2, mode=mode1)
        directions_b = self.get_directions(gmaps, address2, address1, mode=mode2)

        #would be great if this and directions were stored in Part. Class
        #returns typle (substeps, time)
        steps_a, time_a = self.get_steps_and_time(directions_a)
        steps_b, time_b = self.get_steps_and_time(directions_b)

        total_time = time_a + time_b

        #may not to keep track of latlongs anymore
        latlngs_a, potential_dest_a = self.get_potential_destinations(
            steps_a, total_time, gmaps, apikey)
        latlngs_b, potential_dest_b = self.get_potential_destinations(
            steps_b, total_time, gmaps, apikey)
        potential_dest = dict(potential_dest_a, **potential_dest_b)

        #Step 2: Get the times from each participant to each potential destination
        to_try = []
        for k, v in potential_dest.items():
            if len(to_try) < 20:
                to_try.append(v['address'])

        matrix_a = self.get_matrix(gmaps, address1, to_try, mode1)
        matrix_b = self.get_matrix(gmaps, address2, to_try, mode2)


        found_result, rv = self.get_results(matrix_a, matrix_b, gmaps)

        #Step 3: If good results found, create and add destination objects.
        #Otherwise, return None and try again.
        if found_result:
            final = self.map_addresses(rv, potential_dest)
            for d, v in final.items():
                dest = Destination.objects.create(
                    address = d, a_time = v['a_mins'],
                    b_time = v['b_mins'],
                    latlng = v['latlng'],
                    name = v['name'],
                    place_id = v['place_id'],
                    score = round(v['score']),
                    avg_time = round((v['a_mins'] + v['b_mins'])/2))
                dest.save()
                self.destinations.add(dest)
        else:
            #rv = best_address
            #rewrite with midpoint being passed into get potential destinations
            return None

    def get_potential_destinations(self, steps, time, gmaps, apikey):
        '''
        returns a tuple of potential destinations (dicts) and list of latlongs
        '''
        #returns latlongs
        midpoint = self.get_midpoint(steps, time)
        places_dict = {
            'key': apikey,
            'location': midpoint,
            'rankby': 'distance',
            'types': self.business_type}
        latlngs, dest_dict = self.get_places(places_dict, gmaps)
        return latlngs, dest_dict


    def map_addresses(self, results, dests):
        keys = {}
        for address in results.keys():
            short_ad = re.search('\w+[\w\s]+,', address)
            pat = "^" + short_ad.group()
            for k, v in dests.items():
                match = re.search(pat, v['address'])
                if match:
                    if address not in keys:
                        keys[address] = k
        final_rv = {}
        for k, v in keys.items():
            final_rv[k] = {"latlng": v,
                "name": dests[v]['name'],
                'place_id': dests[v]['place_id'],
                'a_mins': results[k]['a_mins'],
                'b_mins': results[k]['b_mins'],
                'score': 100 - (results[k]['score'] * 100)}
        return final_rv


    def bisect(self, target_time, current_time, step):
        time_left = target_time - current_time
        duration = step['duration']['value']
        start_lat = step['start_location']['lat']
        start_lng = step['start_location']['lng']
        end_lat = step['end_location']['lat']
        end_lng = step['end_location']['lng']
        ratio = time_left / duration
        add_lat = ratio*(end_lat - start_lat)
        add_lng = ratio*(end_lng - start_lng)
        new_lat = start_lat + add_lat
        new_lng = start_lng + add_lng
        s = str(new_lat) + "," + str(new_lng)
        return s

    def get_directions(self, client, origin, destination, mode='transit'):
        return client.directions(origin, destination, mode=mode)


    def get_steps_and_time(self, directions):
        legs = directions[0]['legs']
        time = legs[0]['duration']['value']
        steps = legs[0]['steps']
        substeps = self.get_substeps(steps)
        return substeps, time


    def get_substeps(self, steps):
        substeps = []
        for x in steps:
            if 'steps' in x.keys():
                for substep in x['steps']:
                    substeps.append(substep)
            else:
                substeps.append(x)
        return substeps


    def get_midpoint(self, steps, total_time):
        target_time = total_time / 4
        current_time = 0
        for step in steps:
            duration = step['duration']['value']
            end_time = current_time + duration
            if end_time < target_time:
                current_time = end_time
                continue
            return self.bisect(target_time, current_time, step)


    def get_places(self,args, gmaps):
        # use Requests instead of googlemaps package here because package requires
        # a query string, which we don't want
        r = requests.get(
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json?",
            params = args)
        data = r.json()
        latlngs, dest_dict = self.parse_places(data, gmaps)
        return latlngs, dest_dict


    def parse_places(self, places, gmaps):
        rv = []
        dest_dict = {}
        for p in places["results"]:
            lat = p['geometry']['location']['lat']
            lng = p['geometry']['location']['lng']
            name = p['name']
            place_id = p['place_id']
            coords = str(lat) + "," + str(lng)
            r = gmaps.place(place_id)
            address = r['result']['formatted_address']
            rv.append(coords)
            dest_dict[coords] = {'name': name, 'place_id': place_id, 'address': address}
        return rv, dest_dict


    def get_matrix(self, client, origins, destinations, mode='transit'):
        matrix = client.distance_matrix(origins, destinations, mode=mode)
        return matrix


    def get_results(self, matrix_a, matrix_b, gmaps):
        ADDRESS = 0
        SCORE = 1
        scores = {}
        addresses = matrix_a['destination_addresses']
        a_times = matrix_a['rows'][0]['elements']
        b_times = matrix_b['rows'][0]['elements']
        best = (None, 0)

        for i, address_i in enumerate(addresses):
            a_time = a_times[i]['duration']['value']
            b_time = b_times[i]['duration']['value']
            if a_time <= b_time:
                this_score = 1 - (a_time/b_time)
            else:
                this_score = 1 - (b_time/a_time)
            scores[address_i] = {
                'a_mins': a_time /60,
                'b_mins': b_time/60,
                'score': this_score}
            if this_score > best[SCORE]:
                best = (address_i, this_score)
        return_values = {}
        for k, v in scores.items():
            if len(return_values) < 5:
                if v['score'] < 0.2:
                    return_values[k] = v
        if len(return_values) == 0:
            found_result = False
            return found_result, best[ADDRESS]
        else:
            found_result = True
            return found_result, return_values

    def __str__(self):
        return "%s " % (self.trip_id)
