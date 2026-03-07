#! /usr/bin/env python

import sys, os
from dotenv import load_dotenv
import re

load_dotenv()


FGPSCORE = os.path.join("in_game", "common", "auto_modifiers", "country.txt")
FINPUT  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FGPSCORE)
FOUTPUT = os.path.join(os.getenv("SLURROPA_FOLDER"), FGPSCORE)

with open(FINPUT, 'r') as foo:
    gpscore = foo.read()

def half_value(match):
    prefix = match.group(1)
    value_str = match.group(2)
    suffix = match.group(3)
    
    # Convert to float, divide by 2, and format back to string
    new_value = float(value_str) / 2
    
    # We use f-string formatting to ensure we don't get 
    # weird scientific notation like 5e-03
    return f"{prefix}{new_value:g}{suffix}"

pattern = r"(country_control_scaled_population\s*=\s*\{.*?great_power_score\s*=\s*)([\d.]+)(.*?\})"
gpscore = re.sub(pattern, half_value, gpscore, flags=re.DOTALL)

def div_value_2_5(match):
    prefix = match.group(1)
    value_str = match.group(2)
    suffix = match.group(3)
    
    # Convert to float, divide by 2.5, and format back to string
    new_value = float(value_str) / 2.5
    
    # We use f-string formatting to ensure we don't get 
    # weird scientific notation like 5e-03
    return f"{prefix}{new_value:g}{suffix}"

pattern = r"(country_total_army_levy_size\s*=\s*\{.*?great_power_score\s*=\s*)([\d.]+)(.*?\})"
gpscore = re.sub(pattern, div_value_2_5, gpscore, flags=re.DOTALL)


if not os.path.exists(os.path.dirname(FOUTPUT)):
    os.makedirs(os.path.dirname(FOUTPUT))

with open(FOUTPUT, 'w') as foo:
    foo.write(gpscore)

