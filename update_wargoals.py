#! /usr/bin/env python

import sys, os
from dotenv import load_dotenv
import re

load_dotenv()

FWARGOALS = os.path.join("in_game", "common", "wargoals", "00_default.txt")
FINPUT  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FWARGOALS)
FOUTPUT = os.path.join(os.getenv("SLURROPA_FOLDER"), FWARGOALS)

with open(FINPUT, 'r') as foo:
    wargoals = foo.read()

# Claim throne
pattern = r"(take_capital_claim_throne.*?defender\s*=\s*\{)\s*conquer_cost\s*=\s*[\d.]+"
wargoals = re.sub(pattern, r"\1", wargoals, flags=re.DOTALL)

# Coalition
pattern = r"(superiority_coalition.*?attacker\s*=\s*\{.*?)(conquer_cost\s*=\s*)[\d.]+(.*)"
wargoals = re.sub(pattern, r"\g<1>\g<2>0.6\g<3>",wargoals, flags=re.DOTALL)
pattern = r"(superiority_coalition.*?attacker\s*=\s*\{.*?)(subjugate_cost\s*=\s*)[\d.]+(.*)"
wargoals = re.sub(pattern, r"\g<1>\g<2>0.4\g<3>",wargoals, flags=re.DOTALL)

if not os.path.exists(os.path.dirname(FOUTPUT)):
    os.makedirs(os.path.dirname(FOUTPUT))

with open(FOUTPUT, 'w') as foo:
    foo.write(wargoals)

