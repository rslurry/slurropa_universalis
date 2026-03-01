#! /usr/bin/env python

import sys, os
import copy
from lib import locations as L
from dotenv import load_dotenv
import re

load_dotenv()


FHUNDREDYEARS = os.path.join("in_game", "events", "situations", "hundred_years_war.txt")
FINPUT  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FHUNDREDYEARS)
FOUTPUT = os.path.join(os.getenv("SLURROPA_FOLDER"), FHUNDREDYEARS)


# Read in the vanilla location data
with open(FINPUT, 'r') as foo:
    hundredyears_data = foo.read()

pattern = r'(name\s*=\s*hundred_years_war\.208\.d[\s\S]*?ai_chance\s*=\s*\{\s*base\s*=\s*10)'
replacement = r'''\1
            modifier = {
                factor = 0
                scope:actor = { is_human = yes }
            }'''

hundredyears_data = re.sub(pattern, replacement, hundredyears_data)

# Save out the modified event data
if not os.path.exists(os.path.dirname(FOUTPUT)):
    os.makedirs(os.path.dirname(FOUTPUT))

with open(FOUTPUT, 'w') as foo:
    foo.write(hundredyears_data)

