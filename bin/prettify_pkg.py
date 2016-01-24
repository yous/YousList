#!/usr/bin/env python
import os
import json
import collections

pwd = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(pwd)
try:
    f = open(os.path.join(root, 'Rules.1blockpkg'))
    obj = json.load(f, object_pairs_hook=collections.OrderedDict)
    try:
        json_file = open(os.path.join(root, 'Rules.1blockpkg.json'), 'w')
        json.dump(obj, json_file, indent=4, separators=(',', ': '))
    finally:
        json_file.close()
finally:
    f.close()
