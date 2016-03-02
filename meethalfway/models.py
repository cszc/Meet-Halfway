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
        return "%s %s" % (self.street, self.city)

class Participant(models.Model):
    TRANSIT_TYPES = (
        ("walking", "Walking"),
        ("transit", "Public Transit"),
        ("driving", "Driving"),
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

class Meeting(models.Model):
    BUSINESS_TYPES = (
        ("cafe", "Cafe"),
        ("bar", "Bar"),
        ("restaurant", "Restaurant"),
        )
    participant_one = models.ForeignKey(Participant, related_name = 'participant_one', null = True, blank =  True)
    participant_two = models.ForeignKey(Participant, related_name = 'participant_two', null = True, blank = True)
    business_type = models.CharField(max_length=64, null=True, blank=True, choices = BUSINESS_TYPES)
    trip_id = models.CharField(max_length = 100, null=True, blank = True)
    destinations = models.ManyToManyField(Destination, null=True, blank = True)

    def set_participant_two(self, participant):
        self.participant_two = participant

    def get_id(self):
        return self.id

    def random_words(self):
        rw =  RandomWords()
        w1 = rw.random_word()
        w2 = rw.random_word()
        w3 = rw.random_word()
        return w1 + "-" + w2 + "-" + w3

    def get_destinations(self):
        with open('apikeys.txt', 'r') as f:
            apikey = f.readline()
        gmaps = googlemaps.Client(key=apikey)
        address1 = self.participant_one.address
        address2 = self.participant_two.address

        latlngs_a, potential_dest_a = self.get_potential_destinations(address1, address2, gmaps, apikey)
        latlngs_b, potential_dest_b = self.get_potential_destinations(address2, address1, gmaps, apikey)
#         print(potential_dest_a)
#         print(potential_dest_b)
        potential_dest = dict(potential_dest_a, **potential_dest_b)

        to_try = []
        for k,v in potential_dest.items():
            if len(to_try) < 20:
                to_try.append(v['address'])

        matrix_a = get_matrix_via_car(gmaps, address1, to_try)
        matrix_b = get_matrix_via_car(gmaps, address2, to_try)

        found_result, rv = get_results(matrix_a, matrix_b, gmaps)
        if found_result:
#             print("**results**")
#             print(rv)
            final = map_addresses(rv, potential_dest)
            for d in final.keys():
                dest = Destination.object.create(address = d, a_time = d['a_mins'], b_time = d['b_mins'],
                    latlng = d['latlng'], name = d['name'], place_id = d['place_id'])
                dest.save()
                self.destinations.add(dest)
        else:
            return None

    def get_potential_destinations(self, address1, address2, gmaps, apikey):
        '''
        returns a tuple of potential destinations (dicts) and list of latlongs
        '''
        #returns pseudo json and dicts
        directions = get_directions(gmaps, address1, address2)
        #returns tuple (substeps, time)
        steps, time = get_steps_and_time(directions)
        #returns latlongs
        midpoint = get_midpoint(steps, time)
        places_dict = {'key': apikey, 'location': midpoint, 'rankby': 'distance', 'types': self.business_type}
        latlngs, dest_dict = get_places(places_dict, gmaps)
        return latlngs, dest_dict

    @staticmethod
    def map_addresses(results, dests):
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
            final_rv[k] = {"latlng": v, "name": dests[v]['name'], 'place_id': dests[v]['place_id'], 'a_mins': results[k]['a_mins'], 'b_mins': results[k]['b_mins']}
        return final_rv

    @staticmethod
    def bisect(target_time, current_time, step):
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

    @staticmethod
    def get_directions(client, origin, destination, mode='transit'):
        return client.directions(origin, destination, mode)

    @staticmethod
    def get_steps_and_time(directions):
        legs = directions[0]['legs']
        time = legs[0]['duration']['value']
        steps = legs[0]['steps']
        substeps = get_substeps(steps)
        return substeps, time

    @staticmethod
    def get_substeps(steps):
        substeps = []
        for x in steps:
            if 'steps' in x.keys():
                for substep in x['steps']:
                    substeps.append(substep)
            else:
                substeps.append(x)
        return substeps

    @staticmethod
    def get_midpoint(steps, total_time):
        target_time = total_time / 2
        current_time = 0
        for step in steps:
            duration = step['duration']['value']
            end_time = current_time + duration
    #             print(end_time)
            if end_time < target_time:
                current_time = end_time
                continue
            return bisect(target_time, current_time, step)

    @staticmethod
    def get_places(args, gmaps):
        r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?", params = args)
        data = r.json()
        latlngs, dest_dict = parse_places(data, gmaps)
        return latlngs, dest_dict

    @staticmethod
    def parse_places(places, gmaps):
        rv = []
        dest_dict = {}
        for p in places["results"]:
            lat = p['geometry']['location']['lat']
            lng = p['geometry']['location']['lng']
            name = p['name']
            place_id = p['place_id']
    #         print(place_id)
            coords = str(lat) + "," + str(lng)
            r = gmaps.place(place_id)
    #         print(r)
    #         if 'result'
            address = r['result']['formatted_address']
            rv.append(coords)
            dest_dict[coords] = {'name': name, 'place_id': place_id, 'address': address}
        return rv, dest_dict

    @staticmethod
    def get_matrix_via_car(client, origins, destinations, mode='driving'):
        matrix = client.distance_matrix(origins, destinations, mode)
        return matrix

    #via public transportation
    @staticmethod
    def get_matrix_via_transit(client, origins, destinations, mode='transit'):
        matrix = client.distance_matrix(origins, destinations)
        return matrix

    @staticmethod
    def get_results(matrix_a, matrix_b, gmaps):
        scores = {}
        addresses = matrix_a['destination_addresses']
        a_times = matrix_a['rows'][0]['elements']
        b_times = matrix_b['rows'][0]['elements']
        best = (None,0)
        for i, a in enumerate(addresses):
            a_time = a_times[i]['duration']['value']
            b_time = b_times[i]['duration']['value']
            if a_time <= b_time:
                score = 1 - (a_time/b_time)
            else:
                score = 1 - (b_time/a_time)
    #         scores.append((a, a_time, b_time, score))
    #         geocode_result = gmaps.geocode(a)
    #         lat = geocode_result[0]['geometry']['location']['lat']
    #         lng = geocode_result[0]['geometry']['location']['lng']
    #         coords = str(lat) + "," + str(lng)
            scores[a] = {'a_mins': a_time /60, 'b_mins': b_time/60, 'score': score}
            if score > best[1]:
                best = (a,score)
        rv = {}
        for k, v in scores.items():
            if len(rv) < 3:
                if v['score'] < 0.2:
                    rv[k] = v
        if len(rv) == 0:
    #         best_scores = sorted(scores, key=lambda tup: tup[3])
            found_result = False
            return found_result, best[0]
        else:
    #         rv = sorted(rv, key=lambda tup: tup[3])
            found_result = True
            return found_result, rv

    def __str__(self):
        return "%s " % (self.destination)
