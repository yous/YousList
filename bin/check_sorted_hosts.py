import sys


class NotSortedError(Exception):
    pass


"""
Check if each section separated by comment has alphabetically sorted lines.
"""
prev_line = None
# Make this script to run in Python 2 and Python 3
with open(sys.argv[1], encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            prev_line = None
            continue
        if not prev_line:
            prev_line = line
            continue
        if prev_line >= line:
            raise NotSortedError("This line is not sorted: " + line)
        prev_line = line
