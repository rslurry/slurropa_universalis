#! /usr/bin/env python

import sys, os
from dotenv import load_dotenv
import re

load_dotenv()

FHRE_ELECTOR = os.path.join("in_game", "common", "international_organization_special_statuses", "hre.txt")
FINPUT_ELECTOR  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FHRE_ELECTOR)
FOUTPUT_ELECTOR = os.path.join(os.getenv("SLURROPA_FOLDER"), FHRE_ELECTOR)

with open(FINPUT_ELECTOR, 'r') as foo:
    hre_elector_data = foo.read()

# Regex to target ONLY the line inside can_bestow_trigger
elector_pattern = r'(can_bestow_trigger\s*=\s*{[^}]*?)government_type\s*=\s*government_type:monarchy'

elector_replacement = r"""\1OR = {
        government_type = government_type:monarchy
        government_type = government_type:republic
    }"""

hre_elector_data = re.sub(elector_pattern, elector_replacement, hre_elector_data, flags=re.DOTALL)

if not os.path.exists(os.path.dirname(FOUTPUT_ELECTOR)):
    os.makedirs(os.path.dirname(FOUTPUT_ELECTOR))

with open(FOUTPUT_ELECTOR, 'w') as foo:
    foo.write(hre_elector_data)

