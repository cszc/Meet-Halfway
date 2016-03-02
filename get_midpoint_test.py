
# coding: utf-8

# In[163]:

m = meeting()


# In[152]:

testa = {'41.79938610000001,-87.59236039999999': {'place_id': 'ChIJdRVDO2wpDogRC1rjVaM3XUc', 'address': '1369 E 53rd St, Chicago, IL 60615, United States', 'name': 'Cafe 53'}, '41.845301,-87.6275405': {'place_id': 'ChIJCTu5dXAsDogRtPcKzEZHPfE', 'address': '11 W 26th St, Chicago, IL 60616, United States', 'name': 'Awake with Pearl Coffee Cafe'}, '41.7952445,-87.5967496': {'place_id': 'ChIJg1q8LBUpDogRLfJh2h0Xqd4', 'address': '1174 E 55th St, Chicago, IL 60615, United States', 'name': 'Starbucks'}, '41.8168601,-87.6129401': {'place_id': 'ChIJXRITw_0rDogRCeBKoHEqCNk', 'address': '526 E 43rd St, Chicago, IL 60653, United States', 'name': "Ain't She Sweet Cafe"}, '41.81591829999999,-87.64538209999999': {'place_id': 'ChIJSRoRgZ0uDogR2kbuFUqQg4s', 'address': '4305 S Halsted St, Chicago, IL 60609, United States', 'name': 'Bake For Me!'}, '41.83201149999999,-87.61768049999999': {'place_id': 'ChIJJ0_nk_UrDogRA_o8jJch330', 'address': '3428 S King Dr, Chicago, IL 60616, United States', 'name': 'SAPA Coffee & Juice'}, '41.83802060000001,-87.6459921': {'place_id': 'ChIJe0StBUcsDogRiv2PwuXBaVg', 'address': '749 W 31st St, Chicago, IL 60616, United States', 'name': "Dunkin' Donuts"}, '41.8308453,-87.62681189999999': {'place_id': 'ChIJ2ay52Q0sDogRfAXWGul3VvI', 'address': '3506 S State St, Chicago, IL 60609, United States', 'name': 'Starbucks'}, '41.8499141,-87.6316629': {'place_id': 'ChIJU3YycmQsDogRW42Wmb_yF5Q', 'address': '2339 S Wentworth Ave, Chicago, IL 60616, United States', 'name': 'Tasty Place Bakery & Cafe'}, '41.810391,-87.5924261': {'place_id': 'ChIJ2_X3iGMpDogRTNXCwv1fVUk', 'address': '1400 E 47th St, Chicago, IL 60653, United States', 'name': 'DUNKIN DONUTS / BASKIN ROBBINS'}, '41.8412455,-87.6327946': {'place_id': 'ChIJX1eFpW4sDogRGUjNSjU1bN8', 'address': '242 W 29th St, Chicago, IL 60616, United States', 'name': 'HOME'}, '41.850827,-87.63219280000001': {'place_id': 'ChIJozV3jGMsDogRSM65PJ9lQgQ', 'address': '2300 S Wentworth Ave #6, Chicago, IL 60616, United States', 'name': 'China Cafe'}, '41.8361046,-87.6459023': {'place_id': 'ChIJOVdXgEcsDogR-M5ZgDeSswk', 'address': '755 W 32nd St, Chicago, IL 60616, United States', 'name': 'Jackalope Coffee & Tea House'}, '41.803228,-87.5868031': {'place_id': 'ChIJTaIEWXApDogRK7Oe0S2WoWs', 'address': '5030 S Cornell Ave, Chicago, IL 60615, United States', 'name': 'Bridgeport Coffeehouse at the Hyde Park Art Center'}, '41.79984510000001,-87.59106829999999': {'place_id': 'ChIJZ6TpzW0pDogR707HN2TDSrY', 'address': '1418 E 53rd St, Chicago, IL 60615, United States', 'name': "Dunkin' Donuts"}, '41.831542,-87.61466999999999': {'place_id': 'ChIJz9H1xvUrDogRqq6ZTvFqg0A', 'address': '3481 S. Dr Martin L King Jr Dr, Chicago, IL 60616, United States', 'name': "Dunkin' Donuts"}, '41.8519318,-87.6151659': {'place_id': 'ChIJmX6D04YrDogRoGH_APnp5bw', 'address': '2301 S Lake Shore Dr, Chicago, IL 60616, United States', 'name': 'Starbucks'}, '41.80543439999999,-87.5850646': {'place_id': 'ChIJYYHaa3opDogRzmMA-WMLb6k', 'address': '4900 S Lake Shore Dr, Chicago, IL 60615, United States', 'name': 'Lake Shore Cafe'}, '41.7997208,-87.58769749999999': {'place_id': 'ChIJb3glB3IpDogRTunQiOvnkAM', 'address': '1530 E 53rd St, Chicago, IL 60615, United States', 'name': 'Starbucks'}, '41.8453485,-87.62746829999999': {'place_id': 'ChIJCTu5dXAsDogRj1oXXnG854E', 'address': '11 W 26th St, Chicago, IL 60616, United States', 'name': 'South Loop Hotel Chicago'}}
testb = {'41.79938610000001,-87.59236039999999': {'place_id': 'ChIJdRVDO2wpDogRC1rjVaM3XUc', 'address': '1369 E 53rd St, Chicago, IL 60615, United States', 'name': 'Cafe 53'}, '41.790124,-87.605395': {'place_id': 'ChIJ6dpUbjkpDogRSuTvQmsXywA', 'address': 'Dr. Martin Burke, DO #5734, 5758 S Maryland Ave, Chicago, IL 60637, United States', 'name': 'Argo Tea Cafe'}, '41.791214,-87.598317': {'place_id': 'ChIJyyXv8RUpDogRr5NK6ynnehE', 'address': '5706 S University Ave, Chicago, IL 60637, United States', 'name': 'Hallowed Grounds'}, '41.7952445,-87.5967496': {'place_id': 'ChIJg1q8LBUpDogRLfJh2h0Xqd4', 'address': '1174 E 55th St, Chicago, IL 60615, United States', 'name': 'Starbucks'}, '41.80543439999999,-87.5850646': {'place_id': 'ChIJYYHaa3opDogRzmMA-WMLb6k', 'address': '4900 S Lake Shore Dr, Chicago, IL 60615, United States', 'name': 'Lake Shore Cafe'}, '41.7910678,-87.60495069999999': {'place_id': 'ChIJA5vaQjkpDogRKzeBtPUs5QU', 'address': '5700 S Maryland Ave, Chicago, IL 60637, United States', 'name': 'Starbucks'}, '41.7997258,-87.5896854': {'place_id': 'ChIJc7K-5G0pDogR17cplgeY05Y', 'address': '1452 E. 53rd St., Chicago, IL 60615, United States', 'name': 'Greenline Coffee'}, '41.810391,-87.5924261': {'place_id': 'ChIJ2_X3iGMpDogRTNXCwv1fVUk', 'address': '1400 E 47th St, Chicago, IL 60653, United States', 'name': 'DUNKIN DONUTS / BASKIN ROBBINS'}, '41.7900271,-87.5960672': {'place_id': 'ChIJ-bZngRYpDogR_H0Flm9UF6s', 'address': '5751 S Woodlawn Ave, Chicago, IL 60637, United States', 'name': 'Plein Air Cafe'}, '41.7918607,-87.5985003': {'place_id': 'ChIJwZgijBUpDogR5grx29NWWSw', 'address': 'Chicago, IL 60637, United States', 'name': 'Bart Mart (Maroon Market)'}, '41.788996,-87.600951': {'place_id': 'ChIJc0OXzT0pDogRS69W6QZ0RFw', 'address': '5811 S Ellis Ave, Chicago, IL 60637, United States', 'name': 'Cobb Coffee Shop'}, '41.79096270000001,-87.598281': {'place_id': 'ChIJsxLl8RUpDogRrRfARNaP-LU', 'address': '5706 S University Ave, Chicago, IL 60637, United States', 'name': 'Einstein Bros Bagels'}, '41.803228,-87.5868031': {'place_id': 'ChIJTaIEWXApDogRK7Oe0S2WoWs', 'address': '5030 S Cornell Ave, Chicago, IL 60615, United States', 'name': 'Bridgeport Coffeehouse at the Hyde Park Art Center'}, '41.79984510000001,-87.59106829999999': {'place_id': 'ChIJZ6TpzW0pDogR707HN2TDSrY', 'address': '1418 E 53rd St, Chicago, IL 60615, United States', 'name': "Dunkin' Donuts"}, '41.7997993,-87.587142': {'place_id': 'ChIJ7deULnIpDogRWZyB1mG3fQc', 'address': '1558 E 53rd St, Chicago, IL 60615, United States', 'name': 'Ancien Cycles'}, '41.79125849999999,-87.6039156': {'place_id': 'ChIJO_fmTDkpDogRZE5bO_81_xA', 'address': '865-, 899 E 57th St, Chicago, IL 60637, United States', 'name': 'Starbucks'}, '41.79504130000001,-87.58652800000002': {'place_id': 'ChIJhzOc0nIpDogRwG90SnsygTE', 'address': '1603 E 55th St, Chicago, IL 60615, United States', 'name': 'Cafe Corea'}, '41.8168601,-87.6129401': {'place_id': 'ChIJXRITw_0rDogRCeBKoHEqCNk', 'address': '526 E 43rd St, Chicago, IL 60653, United States', 'name': "Ain't She Sweet Cafe"}, '41.7922124,-87.5999337': {'place_id': 'ChIJYXAhOT4pDogRLDyBwiXSGp4', 'address': '1, 1100 E 57th St, Chicago, IL 60637, United States', 'name': 'Ex Libris Cafe'}, '41.7997208,-87.58769749999999': {'place_id': 'ChIJb3glB3IpDogRTunQiOvnkAM', 'address': '1530 E 53rd St, Chicago, IL 60615, United States', 'name': 'Starbucks'}}
testrv = {'4305 S Halsted St, Chicago, IL 60609, USA': {'a_mins': 13.85, 'score': 0.06629213483146068, 'b_mins': 14.833333333333334}, '2339 S Wentworth Ave, Chicago, IL 60616, USA': {'a_mins': 12.466666666666667, 'score': 0.1670378619153675, 'b_mins': 14.966666666666667}, '11 W 26th St, Chicago, IL 60616, USA': {'a_mins': 12.033333333333333, 'score': 0.11951219512195121, 'b_mins': 13.666666666666666}}


# In[155]:

test_dest = dict(testa, **testb)


# In[159]:

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


# In[161]:

map_addresses(testrv, test_dest)


# In[164]:

m.get_destinations()


# In[100]:

apikey = "AIzaSyCuutZJ6_u2Lb8l2WNOJ6zh7BuK_P1CKbU"
gmaps = googlemaps.Client(key=apikey)
r = gmaps.reverse_geocode('ChIJd8BlQ2BZwokRAFUEcm_qrcA', apikey)
x = gmaps.place('ChIJd8BlQ2BZwokRAFUEcm_qrcA')

x['result']['formatted_address']


# In[162]:

import googlemaps
import requests
import csv
import time
import json
import re


apikey = "AIzaSyCuutZJ6_u2Lb8l2WNOJ6zh7BuK_P1CKbU"
start = '121 N LaSalle St, Chicago, IL 60602'
end = 'Harris School of Public Policy, 1155 E 60th St'
transit = 'transit'
    
class meeting:
    address1 = start
    address2 = end
    business_type = 'cafe'


    def get_destinations(self):
    #         with open('apikeys.txt', 'r') as f:
    #             apikey = f.readline()
        apikey = "AIzaSyCuutZJ6_u2Lb8l2WNOJ6zh7BuK_P1CKbU"
        gmaps = googlemaps.Client(key=apikey)
        address1 = self.address1
        address2 = self.address2

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
            return final
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
        #returns ?
        places_dict = {'key': apikey, 'location': midpoint, 'rankby': 'distance', 'types': self.business_type}
        latlngs, dest_dict = get_places(places_dict, gmaps)
        return latlngs, dest_dict
    
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

def get_directions(client, origin, destination, mode='transit'):
    return client.directions(origin, destination, mode)

def get_steps_and_time(directions):
    legs = directions[0]['legs']
    time = legs[0]['duration']['value']
    steps = legs[0]['steps']
    substeps = get_substeps(steps)
    return substeps, time

def get_substeps(steps):
    substeps = []
    for x in steps:
        if 'steps' in x.keys():
            for substep in x['steps']:
                substeps.append(substep)
        else:
            substeps.append(x)
    return substeps

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

def get_places(args, gmaps):
    r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?", params = args)
    data = r.json()
    latlngs, dest_dict = parse_places(data, gmaps)
    return latlngs, dest_dict

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

def get_matrix_via_car(client, origins, destinations, mode='driving'):
    matrix = client.distance_matrix(origins, destinations, mode)
    return matrix

#via public transportation
def get_matrix_via_transit(client, origins, destinations, mode='transit'):
    matrix = client.distance_matrix(origins, destinations)
    return matrix

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

