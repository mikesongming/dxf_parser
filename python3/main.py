#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File Name: dxf_parser.py
# Author: Mike Song
# Created Time: 2018-11-27 17:25:42

import sys

import ezdxf
import shapely
import numpy as np

from .parser import *

supported_dxftypes = ['LWPOLYLINE', 'POLYLINE', 'TEXT', 'MTEXT', 'LINE', 'ARC', 'INSERT', 'HATCH']
dxftype_to_parser = {
        'LWPOLYLINE': parse_lwpolyline, 
        'POLYLINE': parse_polyline, 
        'TEXT': parse_text, 
        'MTEXT': parse_mtext, 
        'LINE': parse_line, 
        'ARC': parse_arc, 
        'INSERT': None, 
        'HATCH': parse_hatch
        }

def parse(filename):
    dwg = ezdxf.readfile('001.dxf')
    msp = dwg.modelspace()

    visible_entities = [e for e in dwg.entities if not e.dxf.invisible]
    entities_by_layer = {e.dxf.layer:[] for e in visible_entities }
    unsupported_entities = {k:[] for k in  entities_by_layer}

    for e in visible_entities:
        if e.dxftype() not in supported_dxftypes:
            unsupported_entities[e.dxf.layer].append(e)
        elif e.dxftype() == 'INSERT':    # block_ref
            supported, unsupported = parse_insert(e)
            entities_by_layer[e.dxf.layer].extend(supported)
            unsupported_entities[e.dxf.layer].extend(unsupported)
        else:
            parser = dxftype_to_parser.get(e.dxftype(), None)
            if parser:
                supported = parser(e)
                entities_by_layer[e.dxf.layer].extend(supported)
            else:
                unsupported_entities[e.dxf.layer].append(e)
    return entities_by_layer, unsupported_entities

def main(dxf_filename):
    return parse(dxf_filename)

if __name__ == "__main__":
    main(sys.argv[0])
