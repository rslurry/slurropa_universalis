#! /usr/bin/env python

import sys, os
from lib import climates as C
from dotenv import load_dotenv

load_dotenv()


FLOCATIONS = os.path.join("in_game", "map_data", "location_templates.txt")
FINPUT  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FLOCATIONS)
FOUTPUT = os.path.join(os.getenv("SLURROPA_FOLDER"), FLOCATIONS)


# Read in the vanilla location data
with open(FINPUT, 'r') as foo:
    location_data = foo.read()

# Update the location data
location_data = C.update_climates(location_data)

# Save out the modified location data
if not os.path.exists(os.path.dirname(FOUTPUT)):
    os.makedirs(os.path.dirname(FOUTPUT))

with open(FOUTPUT, 'w') as foo:
    foo.write(location_data)

