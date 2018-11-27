#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File Name: dxf_parser.py
# Author: Mike Song
# Created Time: 2018-11-27 17:25:42

import sys

import ezdxf
import shapely
import numpy as np

supported_types = ['LWPOLYLINE', 'POLYLINE', 'TEXT', 'MTEXT', 'LINE', 'ARC', 'INSERT', 'HATCH']

def parse(filename):
    dwg = ezdxf.readfile('001.dxf')
    msp = dwg.modelspace()

    visible_entities = [e for e in dwg.entities if not e.dxf.invisible]
    entities_by_layer = {e.dxf.layer:[] for e in visible_entities }
    unsupported_entities = {k:[] for k in  entities_by_layer}

    #TODO
    pass

def main(dxf_filename):
    return parse(dxf_filename)

if __name__ == "__main__":
    main(sys.argv[0])
