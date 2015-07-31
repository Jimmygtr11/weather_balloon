import sys
import time
import json
import math
import ast

import requests


class Predictor:
    def __init__(self, landing_lat, landing_lon):
        '''Initialize coordinates.'''
        self.landing_lat = landing_lat
        self.landing_lon = landing_lon
        self.coords = {}

    def distance(self, a, b):
        '''Return the distance between given coordinates.'''
        return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

    def nearest(self):
        '''Return the coordinates nearest to the desired landing site.'''
        return min(self.coords.keys(), key=lambda x: self.distance(x, (self.landing_lat, self.landing_lon)))

    def generate_coordinate(self, lat, lon):
        '''Calculate starting and landing coordinates based on habhub Predictor.'''
        self.submit_url = 'http://predict.habhub.org/ajax.php?action=submitForm'
        past = '{"valid":"false","error":"A prediction cannot be run for a time that \\n            is in the past"}'
        future = '{"valid":"false","error":"A prediction cannot be run for a time that is \\n            more than 180 hours in the future"}'
        self.payload = {'launchsite' : 'Other',
                        'lat'        : str(lat),
                        'lon'        : str(lon),
                        # Edit values within lines
                        # --------------------------------
                        'initial_alt': '0',  # (m)
                        'hour'       : '15',  # (UTC)
                        'min'        : '0',
                        'second'     : '0',
                        'day'        : '5',
                        'month'      : '8',
                        'year'       : '2015',
                        'ascent'     : '5',  # (m/s)
                        'burst'      : '30000',  # (m)
                        'drag'       : '5',  # (m/s)
                        # --------------------------------
                        'submit'     : 'Run Prediction'}
        r = requests.post(self.submit_url, self.payload)
        try:
            uuid = json.loads(r.text)['uuid']
        except Exception:  # Blank or malformed content was returned. Scrap the coordinate.
            if r.text == past or future:
                print 'Please select a date/time between the current UTC time and 180 hours from now.'
                sys.exit(0)
            else:
                print 'Failed to determine this coordinate.'
                return

        response_url = 'http://predict.habhub.org/ajax.php?action=getCSV&uuid={0}'.format(uuid)
        r = requests.get(response_url)
        try:
            coordinates = ast.literal_eval(r.content)  # Content was originally a list in string representation
            launch_coordinates = float(coordinates[0].split(',')[1]), float(coordinates[0].split(',')[2])
            landing_coordinates = float(coordinates[-2].split(',')[1]), float(coordinates[-2].split(',')[2])

            self.coords[landing_coordinates] = launch_coordinates  # Populates dictionary of Landing: Launch coordinates
            print ('For launch coordinates {0}, you got {1} for landing coordinates.'
                   .format(launch_coordinates, landing_coordinates))
        except Exception:  # Blank or malformed content was returned. Scrap the coordinate.
            print 'Failed to determine this coordinate.'
            return

    def create_X(self, lat, lon, incr, step, loops):
        '''Create X of points.'''
        self.generate_coordinate(lat, lon)
        for _ in range(loops):
            self.generate_coordinate(lat+incr, lon+incr)
            self.generate_coordinate(lat-incr, lon-incr)
            self.generate_coordinate(lat-incr, lon+incr)
            self.generate_coordinate(lat+incr, lon-incr)
            incr += step

    def run(self):
        '''Program engine.'''
        incr = 1
        step = 1
        loops = 3
        self.create_X(self.landing_lat, self.landing_lon, incr, step, loops)
        nearest_landing_coordinates = self.nearest()
        nearest_launching_coordinates = self.coords[nearest_landing_coordinates]
        best_landing = nearest_landing_coordinates
        self.coords.clear()
        while True:  # Loop until the 'best coordinate' is repeated
            self.create_X(nearest_launching_coordinates[0], nearest_launching_coordinates[1], incr, step, loops)
            nearest_landing_coordinates = self.nearest()
            nearest_launching_coordinates = self.coords[nearest_landing_coordinates]
            if best_landing != nearest_landing_coordinates:
                best_landing = nearest_landing_coordinates
            else:  # Best coordinate repeated
                if incr == 1:  # Narrowing search to nearest tenth
                    incr = .1
                    step = .1
                    loops = 10
                elif incr == .1:  # Narrowing search to nearest hundredth
                    incr = .01
                elif incr == .01:  # Coordinate to nearest hundredth found
                    print '-' * 100
                    print 'The best launching coordinates are {0}, which lands on {1}'.format(self.coords[best_landing], best_landing)
                    best_lat = self.coords[best_landing][0]
                    best_lon = self.coords[best_landing][1]
                    self.payload['lat'] = str(best_lat)
                    self.payload['lon'] = str(best_lon)
                    r = requests.post(self.submit_url, self.payload)
                    uuid = json.loads(r.text)['uuid']
                    print 'habhub Predictor URL: {0}{1}'.format('http://predict.habhub.org/#!/uuid=', uuid)
                    print 'Google Maps launch site URL: {0}{1}+{2}'.format('https://www.google.com/maps/place/',
                                                               best_lat,
                                                               best_lon)
                    print '-' * 100
                    break
            self.coords.clear()


if __name__ == '__main__':
    lat = float(raw_input('Latitude?\n> '))
    lon = float(raw_input('Longitude?\n> '))
    p = Predictor(lat, lon).run()
