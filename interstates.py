import sys
import json
import requests

from my_pygeocoder.pygeocoder import Geocoder


MAPS_API_URL = "http://maps.googleapis.com/maps/api/directions/json?sensor=false"


def main(params):
    response = requests.get(MAPS_API_URL, params=params)
    if response.status_code != 200:
        return ['Maps API did not return a proper result']
    data = json.loads(response.text)
    with open('sample.json','w') as f:
        f.write(str(data))
    try:
        steps = data['routes'][0]['legs'][0]['steps']
    except:
        # import pdb; pdb.set_trace()
        return ['No results found by maps API']
    lat_lng_pairs = []
    for step in steps:
        location = step['end_location']
        lat_lng_pairs.append((location['lat'], location['lng']))
    return get_states(lat_lng_pairs)


def get_states(lat_lng_pairs):
    states = []
    for pair in lat_lng_pairs:
        lat, lng = pair[0], pair[1]
        try:
            result = Geocoder.reverse_geocode(lat, lng)
        except:
            continue
        if len(states) == 0 or states[-1] != result.state:
            states.append(result.state)
    return states


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Please pass two addresses (strings) following the program name.'
        print 'Example: $python {0} "Minneapolis, MN" "La Jolla, CA"'.format(sys.argv[0])
        exit()
    params = {'origin': sys.argv[1], 'destination': sys.argv[2]}
    print 'Finding shortest path...'
    results = main(params)
    print ' - '.join(results)
