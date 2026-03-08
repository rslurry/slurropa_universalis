#! /usr/bin/env python

import sys, os
from dotenv import load_dotenv
import re

load_dotenv()

FUNLOCKS = os.path.join("in_game", "common", "advances", "region_north_america.txt")
FINPUT  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FUNLOCKS)
FOUTPUT = os.path.join(os.getenv("SLURROPA_FOLDER"), FUNLOCKS)

with open(FINPUT, 'r') as foo:
    unlocks = foo.read()

replacement = """is_capital_copperworking = yes"""

pattern = r"(copperworking.*?potential\s*=\s*\{)\s*is_capital_mesoamerica\s*=\s*yes(.*?\}\s*\n)"
unlocks = re.sub(pattern, rf"\g<1>\n        {replacement}\g<2>", unlocks, flags=re.DOTALL
)

if not os.path.exists(os.path.dirname(FOUTPUT)):
    os.makedirs(os.path.dirname(FOUTPUT))

with open(FOUTPUT, 'w') as foo:
    foo.write(unlocks)

