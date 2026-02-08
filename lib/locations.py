#! /usr/bin/env python

import sys, os
import glob
import re

all_props = ['topography', 'vegetation', 'climate', 'religion', 'culture', 
             'raw_material']


def update_location_properties(location_data, prop=None):
    """
    Inputs
    ------
    location_data: str.
                   Contents of a location_templates.txt file.
    prop: str, list of str, or None.
          Location property/properties to be updated.
          If None, updates all location properties.
          Options: topography, vegetation, climate, religion, 
                   culture, raw_material
    
    Outputs
    -------
    location_data: str.
                   Contents of the updated location_templates.txt file.
    """
    if isinstance(prop, str):
        prop = [prop]
    elif isinstance(prop, list):
        for ip, p in enumerate(prop):
            assert isinstance(p, str), \
                   "All supplied `prop` values must be strings.\nReceived: "+\
                   str(p)+" at index "+ip
    elif prop is not None:
        raise ValueError("Supplied `prop` "+str(prop)+\
              " must be None, a string, or a list.  Received type "+\
              str(type(prop)))
    else:
        # prop is None - do all
        prop = all_props
    for ip, p in enumerate(prop):
        assert p in all_props, \
            "`prop` must be one of "+(str(all_props)
                                      .replace('[','')
                                      .replace(']',''))+\
            ".\nReceived: "+p+" at index "+ip
    
    for ip, p in enumerate(prop):
        fprops = glob.glob(os.path.join('location_data', p, '*.txt'))
        for fprop in fprops:
            this_prop = os.path.basename(fprop).replace('.txt', '')
            with open(fprop, 'r') as foo:
                prop_locs = foo.read()
            prop_locs = prop_locs.replace(' ', '_').strip()
            prop_locs = prop_locs.split('\n')
            for loc in prop_locs:
                if loc not in location_data:
                    raise ValueError(loc + " not found in the location data.")
                location_data = re.sub(r'('+loc+r'\s*=\s*\{[^}]*?'+p+\
                                       r'\s*=\s*)[^\s}]+', r'\1'+this_prop, 
                                       location_data)
    return location_data
    