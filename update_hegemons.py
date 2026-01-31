import sys, os
import glob
import re
from dotenv import load_dotenv

load_dotenv()

FHEGEMON_BASE = os.path.join("in_game", "common", "hegemons")
FINPUT_BASE   = os.path.join(os.getenv("EU5_GAME_FOLDER"))
FOUTPUT_BASE  = os.path.join(os.getenv("SLURROPA_FOLDER"))

hegemons = ['economic', 'naval', 'military', 'diplomatic', 'cultural']

for hegemon in hegemons:
    FHEGEMON = glob.glob(os.path.join(FINPUT_BASE, FHEGEMON_BASE, '*'+hegemon+'*'))
    if len(FHEGEMON) == 1:
        FHEGEMON = FHEGEMON[0]
    else:
        raise ValueError("Number of "+hegemon+" hegemon files found:"+str(len(FHEGEMON))+'\nFiles: '+str(FHEGEMON))
    
    with open(FHEGEMON, 'r') as foo:
        contents = foo.read()
    
    # Disable external diplomatic actions
    contents = contents.replace('allow_diplomacy', '#allow_diplomacy')
    
    # Lose hegemon when someone equals/exceeds you in strength
    #pattern = re.compile( r'([A-Za-z0-9_:]+)\s*>\s*\{\s*' r'value\s*=\s*root\.\1\s*' r'multiply\s*=\s*([0-9.]+)\s*' r'\}', re.DOTALL )
    #replacement = r'\1 >= root.\1'
    #contents = pattern.sub(replacement, contents)
    
    # Gain hegemon only when someone is >=25% stronger than #2
    #pattern = re.compile( r'([A-Za-z0-9_:]+)\s*>\s*root\.\1' )
    #replacement = ( r'\1 > {' r'\n value = root.\1' r'\n multiply = 0.8' r'\n}' )
    #contents = pattern.sub(replacement, contents)
    
    # Save it
    FOUT = FHEGEMON.replace(FINPUT_BASE, FOUTPUT_BASE)
    if not os.path.exists(os.path.dirname(FOUT)):
        os.makedirs(os.path.dirname(FOUT))
    with open(FOUT, 'w') as foo:
        foo.write(contents)

