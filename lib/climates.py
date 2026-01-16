#! /usr/bin/env python

import sys, os
import glob
import re

def update_climates(location_data):
    fclimates = glob.glob(os.path.join('climates', '*.txt'))
    for fclimate in fclimates:
        climate = os.path.basename(fclimate).replace('.txt', '')
        with open(fclimate, 'r') as foo:
            climate_locs = foo.read()
        climate_locs = climate_locs.replace(' ', '_').strip()
        climate_locs = climate_locs.split('\n')
        for loc in climate_locs:
            if loc not in location_data:
                raise ValueError(loc + " not found in the location data.")
            location_data = re.sub(r'('+loc+r'\s*=\s*\{[^}]*?climate\s*=\s*)[^\s}]+', r'\1'+climate, location_data)
    return location_data

