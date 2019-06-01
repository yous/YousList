# -*- coding=utf-8 -*-
#!/usr/bin/env python
import os
import io
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
    f = io.open(os.path.join(root, 'Rules.1blockpkg.json'), encoding='utf-8')
    obj = json.load(f, object_pairs_hook=OrderedDict)
    try:
        pkg_file = open(os.path.join(root, 'Rules.1blockpkg'), 'w')
        json.dump(obj, pkg_file, separators=(',', ':'))
    finally:
        pkg_file.close()
finally:
    f.close()
