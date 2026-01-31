#! /usr/bin/env python

import sys, os
from dotenv import load_dotenv
import re

load_dotenv()

FHRE_SPECSTATUS = os.path.join("in_game", "common", "international_organization_special_statuses", "hre.txt")
FINPUT_SPECSTATUS  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FHRE_SPECSTATUS)
FOUTPUT_SPECSTATUS = os.path.join(os.getenv("SLURROPA_FOLDER"), FHRE_SPECSTATUS)

with open(FINPUT_SPECSTATUS, 'r') as foo:
    hre_specstatus_data = foo.read()

# Regex to target ONLY the line inside can_bestow_trigger
elector_pattern = r'(can_bestow_trigger\s*=\s*{.*?\n)(\s*)government_type\s*=\s*government_type:monarchy'

elector_replacement = r"""\1\2OR = {
\2\tgovernment_type = government_type:monarchy
\2\tgovernment_type = government_type:republic
\2}"""

hre_specstatus_data = re.sub(elector_pattern, elector_replacement, hre_specstatus_data, flags=re.DOTALL)

rescind_pattern = r'(\s*)NOT\s*=\s*{\s*government_type\s*=\s*government_type:monarchy\s*}'
rescind_replacement = r"""\1NOT = {
\1\tOR = {
\1\t\tgovernment_type = government_type:monarchy
\1\t\tgovernment_type = government_type:republic
\1\t}
\1}"""

rescind_pattern = r'\n(\s*)NOT\s*=\s*{\s*government_type\s*=\s*government_type:monarchy\s*}\n'
rescind_replacement = (
    r"\n\1NOT = {\n"
    r"\1\tOR = {\n"
    r"\1\t\tgovernment_type = government_type:monarchy\n"
    r"\1\t\tgovernment_type = government_type:republic\n"
    r"\1\t}\n"
    r"\1}\n"
)

hre_specstatus_data = re.sub(rescind_pattern, rescind_replacement, hre_specstatus_data)

if not os.path.exists(os.path.dirname(FOUTPUT_SPECSTATUS)):
    os.makedirs(os.path.dirname(FOUTPUT_SPECSTATUS))

with open(FOUTPUT_SPECSTATUS, 'w') as foo:
    foo.write(hre_specstatus_data)

