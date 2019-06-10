# -*- coding=utf-8 -*-
import io
import re
import sys

"""
Check if each section separated by comment has alphabetically sorted lines.
"""
prev_line = None
# Make this script to run in Python 2 and Python 3
with io.open(sys.argv[1], 'r', encoding='utf-8') as f:
    filestream = f.readlines()

for line in filestream:
    line = line.strip()
    if not line or line.startswith('!') or re.match(r'\[Adblock.*\]', line):
        prev_line = None
        continue
    if not prev_line:
        prev_line = line
        continue
    if prev_line >= line:
        raise Exception('This line is not sorted: ' + line)
    prev_line = line
