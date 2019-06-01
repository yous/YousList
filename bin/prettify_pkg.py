#!/usr/bin/env python
# -*- coding=utf-8 -*-
import io
import os
import sys

if sys.version_info[:2] >= (2, 7):
    import json
    from collections import OrderedDict
else:
    import simplejson as json
    from ordereddict import OrderedDict

pwd = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(pwd)
try:
    f = io.open(os.path.join(root, 'Rules.1blockpkg'), encoding='utf-8')
    obj = json.load(f, object_pairs_hook=OrderedDict)
    try:
        json_file = open(os.path.join(root, 'Rules.1blockpkg.json'), 'w')
        json.dump(obj, json_file, indent=4, separators=(',', ': '))
    finally:
        json_file.close()
finally:
    f.close()
