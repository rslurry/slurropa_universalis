#! /usr/bin/env python

import sys, os
from dotenv import load_dotenv
import re

load_dotenv()

##### International Organization file
FHRE = os.path.join("in_game", "common", "international_organizations", "hre.txt")
FINPUT_HRE  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FHRE)
FOUTPUT_HRE = os.path.join(os.getenv("SLURROPA_FOLDER"), FHRE)

with open(FINPUT_HRE, 'r') as foo:
    hre_data = foo.read()

hre_data = hre_data.replace("great_power_score_exempt_from_forfeit = 250", "great_power_score_exempt_from_forfeit = 150")

if not os.path.exists(os.path.dirname(FOUTPUT_HRE)):
    os.makedirs(os.path.dirname(FOUTPUT_HRE))

with open(FOUTPUT_HRE, 'w') as foo:
    foo.write(hre_data)


##### International Organization Special Statuses file
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


##### Dismantle HRE file
FDISMANTLE = os.path.join("in_game", "common", "peace_treaties", "dismantle_hre.txt")
FINPUT_DISMANTLE  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FDISMANTLE)
FOUTPUT_DISMANTLE = os.path.join(os.getenv("SLURROPA_FOLDER"), FDISMANTLE)

with open(FINPUT_DISMANTLE, 'r') as foo:
    hre_dismantle_data = foo.read()


count_limit=400 # min # HRE provinces to disable dismantle peace deal
# Find the allow = { start
m = re.search(r'allow\s*=\s*\{', hre_dismantle_data)
if not m:
    raise ValueError("Dismantle HRE file: Unable to find allow block.")

start = m.start()
brace_start = m.end() - 1  # position of the '{'

# Determine indentation of the allow line
line_start = hre_dismantle_data.rfind("\n", 0, start)
base_indent = "" if line_start == -1 else hre_dismantle_data[line_start+1:start]

# Find the matching closing brace
depth = 0
i = brace_start
while i < len(hre_dismantle_data):
    if hre_dismantle_data[i] == "{":
        depth += 1
    elif hre_dismantle_data[i] == "}":
        depth -= 1
        if depth == 0:
            break
    i += 1

if depth != 0:
    # malformed block
    raise ValueError("Dismantle HRE file: Unable to find closing } for allow block.")

# Extract original inner content
inner = hre_dismantle_data[brace_start+1:i]

# Detect indentation of inner block
m2 = re.search(r"\n([ \t]*)\S", inner)
inner_indent = m2.group(1) if m2 else base_indent + "    "

inner_splt = inner.split('\n')
for ii in range(len(inner_splt)):
    inner_splt[ii] = f"{base_indent}{inner_splt[ii]}"
inner = '\n'.join(inner_splt)

# Build new block
new_block = (
    f"allow = {{\n"
    f"{inner_indent}OR = {{{inner}\n"
    f"{inner_indent}    international_organization:hre = {{\n"
    f"{inner_indent}        any_international_organization_owned_location = {{\n"
    f"{inner_indent}            count < {count_limit}\n"
    f"{inner_indent}        }}\n"
    f"{inner_indent}    }}\n"
    f"{inner_indent}}}\n"
    f"{base_indent}}}"
)

# Replace the original block
hre_dismantle_data = hre_dismantle_data[:start] + new_block + hre_dismantle_data[i+1:]

if not os.path.exists(os.path.dirname(FOUTPUT_DISMANTLE)):
    os.makedirs(os.path.dirname(FOUTPUT_DISMANTLE))

with open(FOUTPUT_DISMANTLE, 'w') as foo:
    foo.write(hre_dismantle_data)
