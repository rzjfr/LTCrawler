"""
finds book catalogs for all members of a given work id and saves them in html
files: "./data/profile/catalog/*.html"
"""
import users
import books
import json
import sys
from helpers import *

try:
    work = sys.argv[1]
except:
    work = '306947'
members = books.find_all_members(work)  # all members of given work
members = remove_duplicate(members)
print len(members)
i = 0
for member in members:
    i += 1
    print '%d of %d, %s' % (i, len(members), member)
    users.find_books(member)
