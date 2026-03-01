#! /usr/bin/env python

import sys, os
import copy
from lib import locations as L
from dotenv import load_dotenv
import re

load_dotenv()


FFORMABLES = os.path.join("in_game", "common", "formable_countries", "00_formable_countries.txt")
FINPUT  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FFORMABLES)
FOUTPUT = os.path.join(os.getenv("SLURROPA_FOLDER"), FFORMABLES)


# Read in the vanilla location data
with open(FINPUT, 'r') as foo:
    formables_data = foo.read()

# 1. Extract the FRA_f block
fra_pattern = r'(FRA_f\s*=\s*\{)([\s\S]*?)(\n\})'
match = re.search(fra_pattern, formables_data)

if match:
    start, fra_body, end = match.groups()

    # 2. Update required_locations_fraction inside FRA_f
    fra_body = re.sub(
        r'(required_locations_fraction\s*=\s*)[\d.]+',
        r'\g<1>0.5',
        fra_body
    )

    # 3. Replace the allow block inside FRA_f
    fra_body = re.sub(
        r'allow\s*=\s*\{[\s\S]*?\}',
        r'''allow = {
        owns = location:paris

        region:france_region = {
            any_location_in_region = {
                is_owned_or_owned_by_subjects_or_below_of = root
                count >= 335
            }
        }
    }''',
        fra_body
    )

    # 4. Reassemble the FRA_f block
    new_fra_block = start + fra_body + end

    # 5. Replace the old FRA_f block in the full file
    formables_data = re.sub(fra_pattern, new_fra_block, formables_data)
else:
    raise ValueError("FRA_f block not found.")

# Save out the modified event data
if not os.path.exists(os.path.dirname(FOUTPUT)):
    os.makedirs(os.path.dirname(FOUTPUT))

with open(FOUTPUT, 'w') as foo:
    foo.write(formables_data)

