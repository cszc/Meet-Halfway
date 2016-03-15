from django.db import models
import requests
import json
import time
import re
import googlemaps
import csv
from random_words import RandomWords
import pyusps_modified

#reading in apikey
with open('apikeys.txt', 'r') as f:
    APIKEY = f.readline().strip()

#initializing google maps client
GMAP = googlemaps.Client(key=APIKEY)

class Address(models.Model):
    '''
    Address class holds four attributes for street, city, state, and zip.
    Method verify_address uses PYUSPS to validate address.
    '''
    street = models.CharField(max_length = 64)
    city = models.CharField(max_length = 64)
    state = models.CharField(max_length = 2)
    zip_code = models.CharField(max_length = 5)

    def verify_address(self):
        '''
        Uses PYUSPS to verify addresses.
        '''
        verify = True
        address = ""
        suggestion = ""
        with open('uspskey.txt', 'r') as f:
            uspskey = f.readline().strip()
        addr = dict([
            ('address', self.street),
            ('city', self.city),
            ('state', self.state),
            ('zip_code', self.zip_code),
            ])
        try:
            address = pyusps_modified.verify(uspskey,addr)

        except ValueError as e:
            verify = False
            if "-2147219402" in str(e):
                suggestion = "Check your state field entry"
            if "-2147219403" in str(e):
                suggestion = "This address matches more than one address. Please use a different address."
            if "-2147219401" in str(e):
                suggestion = "No address found at this location."
            if  "-2147219400" in str(e):
                suggestion = "Check your city field entry"

        return verify, suggestion, address

    def __str__(self):
        return "%s %s %s %s" % (self.street, self.city, self.state, self.zip_code)

class Participant(models.Model):
    '''
    Particpant model contains two attributes: transit mode and starting location
    (an instance of the Address class).
    '''
    TRANSIT_TYPES = (
        ("walking", "Walking"),
        ("transit", "Public Transit"),
        ("driving", "Driving"),
        ("bicycling", "Bicycling")
        )
    starting_location = models.ForeignKey(Address, null=True, blank = True)
    transit_mode = models.CharField(max_length = 70, choices = TRANSIT_TYPES)

    def get_id(self):
        return self.id

class Destination(models.Model):
    '''
    An instance of destination is created for each potential meeting place
    that meets the given criteria and holds several attributes.
    '''
    address = models.CharField(max_length = 100, null=True, blank = True)
    a_time = models.CharField(max_length = 3, null=True, blank = True)
    b_time = models.CharField(max_length = 3, null=True, blank = True)
    latlng = models.CharField(max_length = 64, null=True, blank = True)
    name = models.CharField(max_length = 64, null=True, blank = True)
    place_id = models.CharField(max_length = 64, null=True, blank = True)
    score = models.CharField(max_length = 3, null=True, blank = True)
    avg_time = models.CharField(max_length = 3, null=True, blank = True)

class Meeting(models.Model):
    '''
    An instance of a meeting contains two participants, a business type,
    trip id, and up to five instances of the Destination class.

    It also contains several methods for finding the midpoint and destinations.
    '''
    BUSINESS_TYPES = (
        ("cafe", "Cafe"),
        ("bar", "Bar"),
        ("restaurant", "Restaurant"),
        ("book_store", "Book Store"),
        ("gas_station", "Gas Station"),
        ("library", "Library")
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

    def set_participant_two(self, participant):
        self.participant_two = participant

    def get_id(self):
        return self.id

    def random_words(self):
        '''
        Generates three random words for meeting id and url creation
        Outputs: meeting id (a string)
        '''
        rw =  RandomWords()
        w1 = rw.random_word()
        w2 = rw.random_word()
        w3 = rw.random_word()
        return w1 + "-" + w2 + "-" + w3

    def get_destinations(self):
        '''
        Creates up to 5 valid potential destinations for a Meeting object
        that has two complete participants and starting addresses.

        Returns None if no solution found
        '''
        address1 = str(self.participant_one.starting_location)
        address2 = str(self.participant_two.starting_location)

        #Returns none if participants enter same address for both
        if address1==address2:
            return None

        mode1 = self.participant_one.transit_mode
        mode2 = self.participant_two.transit_mode

        #Step 1: Get potential destinations based on midpoint for each participant
        #returns a dict and total time
        potential_destinations = self.get_all_destinations(
            address1, address2, mode1, mode2)
        if len(potential_destinations) == 0:
            return None

        #Step 2: Get the times from each participant to each potential destination
        found_result, destinations = self.test_matrices(
            potential_destinations, address1, address2, mode1, mode2)

        #Step 3: If good results found, create and add destination objects.
        #Otherwise, return None and try again.
        if found_result:
            self.create_destinations(destinations, potential_destinations)
        else:
            #Tries as second time from Step 2. If fails, returns None
            new_midpoint = destinations
            potential_destinations2 = self.get_potential_destinations(midpoint = new_midpoint)
            found_result2, rv2 = self.test_matrices(potential_destinations2, address1, address2, mode1, mode2)
            if found_result2:
                self.create_destinations(rv2, potential_destinations2)
            else:
                return None


    def get_target_time(self, time_a, time_b):
        '''
        Calculates the target travel time for each participant

        Inputs:
            time_a: travel time (seconds) for first participant to second address
            time_b: travel time for second participant to first address
        Outputs:
            target time in seconds
        '''
        total_time = time_a + time_b
        target_time = (time_a / total_time) * time_b
        return target_time


    def get_all_destinations(self, address1, address2, mode1, mode2):
        '''
        Step One of the algorithm.
        First, it determines a target time by getting directions
        from starting address one to starting address two and vice versa.
        Then, it steps along both directions to find two potential midpoints.
        Lastly, it tries to find potential destinations that match criteria
        around the two destinations.
        Returns a dictionary of all potential destinations.
        Inputs:
            address1, address2: instances of Address class
            mode1, mode2: strings
        Outputs:
            potential destinations: dictionary
        '''
        directions_a = self.get_directions(address1, address2, mode=mode1)
        directions_b = self.get_directions(address2, address1, mode=mode2)

        steps_a, time_a = self.get_steps_and_time(directions_a)
        steps_b, time_b = self.get_steps_and_time(directions_b)

        target_time = self.get_target_time(time_a, time_b)

        potential_dest_a = self.get_potential_destinations(
            steps = steps_a, time = target_time)
        potential_dest_b = self.get_potential_destinations(
            steps = steps_b, time = target_time)

        return dict(potential_dest_a, **potential_dest_b)


    def test_matrices(self, potential_dest, address1, address2, mode1, mode2):
        '''
        Given a list of potential desintations, calculates the time of travel
        from each participant to each destination. Then, a call to get_results
        returns and destinations that meet fairness criteria.
        Inputs:
            potential_dest: dictionary of addresses
            address1, address2: each participant's address (instance of Address class)
            mode1, mode2, each participant's mode of transportation (string)
        Outputs:
            Results: Boolean (True if result found) and best meeting places
        '''
        to_try = []
        for k, v in potential_dest.items():
            if len(to_try) < 20:
                to_try.append(v['address'])

        matrix_a = self.get_matrix(address1, to_try, mode1)
        matrix_b = self.get_matrix(address2, to_try, mode2)

        return self.get_results(matrix_a, matrix_b)


    def create_destinations(self, destinations, potential_dest):
        '''
        Creates destinations objects of good destinations are found.
        Inputs:
            destinations: dictionary
            potential_destinations: dictionary
        Outputs:
            Nothing. Saves destination objects to database.
        '''
        final = self.map_addresses(destinations, potential_dest)
        for d, v in final.items():
            dest = Destination.objects.create(
                address = d, a_time = v['a_mins'],
                b_time = v['b_mins'],
                latlng = v['latlng'],
                name = v['name'],
                place_id = v['place_id'],
                score = round(v['score']),
                avg_time = round((v['a_mins'] + v['b_mins']) / 2))
            dest.save()
            self.destinations.add(dest)


    def get_potential_destinations(self, steps=None, time=None, midpoint=None):
        '''
        Gets potential destinations around a lat long using call to Google Places.
        If no midpoint is given, calculates a midpoint using steps and time.
        Inputs:
            steps: Dictionary of steps from Google directions call
            time: Integer
            midpoint: LatLong (string)
        Outputs: Returns a dictionary of potential destinations
        '''
        if not midpoint:
            midpoint = self.get_midpoint(steps, time)
        places_dict = {
            'key': APIKEY,
            'location': midpoint,
            'rankby': 'distance',
            'types': self.business_type}
        dest_dict = self.get_places(places_dict)
        return dest_dict


    def map_addresses(self, results, dests):
        '''
        Matches addresses from results with addresses in a dictionary
        holding information about potential destinations.
        Inputs:
            results: dictionary
            dests: dictionary
        returns:
            final_rv: dictionary
        '''
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
        '''
        Given a target time, current time, and one step from a call to
        Google Directions, returns a latlong as a string for the desired
        location along the path.
        inputs:
            target_time: integer
            current_time: integer
            step: dictionary
        output:
            latlng: string representing latlong
        '''
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
        latlng = str(new_lat) + "," + str(new_lng)
        return latlng


    def get_directions(self, origin, destination, mode='transit'):
        '''
        Given two addresses and a mode of transit, returns a call to Google
        Directions API
        input:
            origin: Address class instance
            destination: Address class instance
            mode: Mode of transportation. Transit is default.
        output:
            List of dictionaries with steps and meta data from Google Directions
            API call
        '''
        return GMAP.directions(origin, destination, mode=mode)


    def get_steps_and_time(self, directions):
        '''
        Pulls out a dictionary of steps and total time traveled from a list of
        dictionaries returned by a Google directions API call.
        input:
            directions: List of dicts from Google Directions API call
        output:
            substeps: list of steps
            time: total time traveled (integer)
        '''
        legs = directions[0]['legs']
        time = legs[0]['duration']['value']
        steps = legs[0]['steps']
        substeps = self.get_substeps(steps)
        return substeps, time


    def get_substeps(self, steps):
        '''
        Returns substeps from given a step from Google Directions.
        input:
            steps: a dictionary containing information about the step from
            Google Directions API call.
        output:
            substeps: list of substeps
        '''
        substeps = []
        for x in steps:
            if 'steps' in x.keys():
                for substep in x['steps']:
                    substeps.append(substep)
            else:
                substeps.append(x)
        return substeps


    def get_midpoint(self, steps, target_time):
        '''
        Given a list of steps from a Google Directions call and a target time,
        returns a lat-long that approximates the spatial point at which the
        target time will be reached.
        inputs:
            steps: list (returned from Google Directions API call)
        outputs:
            lat-long: string
        '''
        current_time = 0
        for step in steps:
            duration = step['duration']['value']
            end_time = current_time + duration
            if end_time < target_time:
                current_time = end_time
                continue
            return self.bisect(target_time, current_time, step)


    def get_places(self, args):
        '''
        Given a starting lat-long, fetch nearby places that fit user requirements from the
        Google Places API
        inputs:
            args: dictionary of arguments for the query
        outputs:
            dest_dict: dictionary of potential destinations and associated information
        '''
        # use Requests instead of googlemaps package here because package requires
        # a query string, which we don't want
        r = requests.get(
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json?",
            params = args)
        data = r.json()
        dest_dict = self.parse_places(data)
        return dest_dict


    def parse_places(self, places):
        '''
        Parse the output of a request to the Google Places API and
        pull out the latlong, address, name, and unique place_id for
        each potential destination
        inputs:
            places: json returned by request to Google Places API
        outputs:
            dest_dict: dictionary of potential destinations and associated information
        '''
        dest_dict = {}
        for p in places["results"]:
            lat = p['geometry']['location']['lat']
            lng = p['geometry']['location']['lng']
            name = p['name']
            place_id = p['place_id']
            coords = str(lat) + "," + str(lng)
            # Get the address by looking up the place ID from the Places API, since the nearby search
            # doesn't return that information in the initial request
            r = GMAP.place(place_id)
            address = r['result']['formatted_address']
            dest_dict[coords] = {'name': name, 'place_id': place_id, 'address': address}
        return dest_dict


    def get_matrix(self, origins, destinations, mode='transit'):
        '''
        Calls the Google Distance Matrix API
        inputs:
            origins:
            destinations:
            mode: defaults to transit
        outputs:
            matrix: List/dictionary object returned by Google Distance Matrix API
        '''
        matrix = GMAP.distance_matrix(origins, destinations, mode=mode)
        return matrix


    def get_results(self, matrix_a, matrix_b):
        '''
        Score potential destinations and return the best results.
        If no satisfactory solutions found, return the best-scoring lat-long
        inputs:
            matrix_a, matrix_b: results of calls to the Google Distance API
        output:
            found_result: Boolean (true if satisfactory solution found)
            destinations: dictionary of destinations or, if nothing found, best address
        '''
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

        destinations = {}
        for k, v in scores.items():
            if len(destinations) < 5:
                if v['score'] < 0.2:
                    destinations[k] = v
        if len(destinations) == 0:
            found_result = False
            return found_result, best[ADDRESS]
        else:
            found_result = True
            return found_result, destinations

    def __str__(self):
        return "%s " % (self.trip_id)
