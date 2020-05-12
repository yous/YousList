# -*- coding=utf-8 -*-
import os
import io
import json
from collections import OrderedDict

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
