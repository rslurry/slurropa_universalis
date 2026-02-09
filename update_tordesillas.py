#! /usr/bin/env python

import sys, os
import copy
from lib import locations as L
from dotenv import load_dotenv

load_dotenv()


FTORDESILLAS = os.path.join("in_game", "events", "situations", "treaty_of_tordesillas.txt")
FINPUT  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FTORDESILLAS)
FOUTPUT = os.path.join(os.getenv("SLURROPA_FOLDER"), FTORDESILLAS)


# Read in the vanilla location data
with open(FINPUT, 'r') as foo:
    tordesillas_data = foo.read()

# Disable treaty_of_tordesillas.1 trigger to ensure the situation never fires
event1_start = tordesillas_data.index("\ntreaty_of_tordesillas.1")
event1_end   = tordesillas_data.index("\ntreaty_of_tordesillas.2")
event1_data = tordesillas_data[event1_start : event1_end]
trigger_start = event1_data[event1_data.index("trigger"):]
# Count { and } to determine where trigger block ends
brace_start = trigger_start.index('{')
# Find the matching closing brace
depth = 0
i = brace_start
while i < len(trigger_start):
    if trigger_start[i] == "{":
        depth += 1
    elif trigger_start[i] == "}":
        depth -= 1
        if depth == 0:
            break
    i += 1

if depth != 0:
    # malformed block
    raise ValueError("Tordesillas event file: Unable to find closing } for trigger block.")

# Extract original trigger content
trigger_content = trigger_start[brace_start+1:i].split('\n')
closing_indent = trigger_content[-1]
# Determine indentation to begin adding comments
for line in trigger_content:
    if not len(line.replace('\t', '')):
        continue
    for ic, c in enumerate(line):
        if c == '\t':
            continue
        else:
            indent = line[:ic]
            break
    break
# Comment out everything
new_trigger_content = copy.deepcopy(trigger_content)
for iline, line in enumerate(new_trigger_content):
    if not len(line.replace('\t', '')):
        continue
    new_trigger_content[iline] = indent + '#' + line[len(indent):]
# New trigger: always = no so it never triggers
new_trigger_content.append(indent+'always = no\n'+closing_indent)
new_trigger_content = '\n'.join(new_trigger_content)
# Update the file data
tordesillas_data = tordesillas_data.replace('\n'.join(trigger_content), new_trigger_content)

# Save out the modified event data
if not os.path.exists(os.path.dirname(FOUTPUT)):
    os.makedirs(os.path.dirname(FOUTPUT))

with open(FOUTPUT, 'w') as foo:
    foo.write(tordesillas_data)

