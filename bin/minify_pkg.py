#!/usr/bin/env python
import os
import json
import collections

pwd = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(pwd)
try:
    f = open(os.path.join(root, 'Rules.1blockpkg.json'))
    obj = json.load(f, object_pairs_hook=collections.OrderedDict)
    try:
        pkg_file = open(os.path.join(root, 'Rules.1blockpkg'), 'w')
        json.dump(obj, pkg_file, separators=(',', ':'))
    finally:
        pkg_file.close()
finally:
    f.close()
