#! /usr/bin/env python

import sys, os
from dotenv import load_dotenv
import re

load_dotenv()

expel_pattern = r'''
        visible\s*=\s*\{      # the visible = { line
        .*?                   # everything inside, non-greedy
        \n\t\t\}              # the closing } of visible with the same indentation
        \n\t\tmap_color       # the next line starts map_color
    '''

expel_replacement = r'''
visible = {
            NOT = { cabinet_already_performing_same_task_on_target = { cabinet_action = expel_people interaction_target = target } }
            expel_people_valid_target = yes
        }
        
        enabled = {
            expel_people_valid_target = yes
        }

        map_color'''.lstrip("\n")

CABINET_ACTIONS = ["expel_people.txt"]
PATTERNS = [expel_pattern]
REPLACEMENTS = [expel_replacement]
FLAGS    = [re.DOTALL | re.VERBOSE]

# Add new requirements for each action
for iaction, action in enumerate(CABINET_ACTIONS):
    FACTION = os.path.join("in_game", "common", "cabinet_actions", action)
    FINPUT  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FACTION)
    FOUTPUT = os.path.join(os.getenv("SLURROPA_FOLDER"), FACTION)

    # Read in the vanilla cabinet action
    with open(FINPUT, 'r') as foo:
        cab_action = foo.read()
    
    pattern = re.compile(PATTERNS[iaction], FLAGS[iaction])
    cab_action = pattern.sub(REPLACEMENTS[iaction], cab_action)
    
    # Save out the modified cabinet action
    if not os.path.exists(os.path.dirname(FOUTPUT)):
        os.makedirs(os.path.dirname(FOUTPUT))

    with open(FOUTPUT, 'w') as foo:
        foo.write(cab_action)

