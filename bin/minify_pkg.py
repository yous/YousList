import json
import os
from collections import OrderedDict

pwd = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(pwd)
with open(os.path.join(root, "Rules.1blockpkg.json"), encoding="utf-8") as f:
    obj = json.load(f, object_pairs_hook=OrderedDict)
    with open(os.path.join(root, "Rules.1blockpkg"), "w") as pkg_file:
        json.dump(obj, pkg_file, separators=(",", ":"))
