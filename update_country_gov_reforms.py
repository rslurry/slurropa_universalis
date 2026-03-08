#! /usr/bin/env python

import sys, os
from dotenv import load_dotenv
import re

load_dotenv()

FREFORMS = os.path.join("in_game", "common", "government_reforms", "country_specific.txt")
FINPUT  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FREFORMS)
FOUTPUT = os.path.join(os.getenv("SLURROPA_FOLDER"), FREFORMS)

with open(FINPUT, 'r') as foo:
    reforms = foo.read()

replacement = """        tax_income_efficiency = -0.1
        global_estate_max_tax = -0.05
        government_reform_slots = 1"""
pattern = r"(ancient_french_taxation.*?country_modifier\s*=\s*\{).*?(\s*\n\s*\}.*?\})"
reforms = re.sub(pattern, rf"\g<1>\n{replacement}\2", reforms, flags=re.DOTALL)

if not os.path.exists(os.path.dirname(FOUTPUT)):
    os.makedirs(os.path.dirname(FOUTPUT))

with open(FOUTPUT, 'w') as foo:
    foo.write(reforms)

