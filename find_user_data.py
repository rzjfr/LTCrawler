"""
finds json data for all members of a given work id form LT json api and saves
them in json formated files: "./data/profile/json/*.json"
"""
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
later = ['Kaethe', 'eandino2012', 'gangleri', 'citizenkelly', 'IslandDave',
         'bpc', 'apswartz', 'mvuijlst', 'reecejones', 'michael.brodesky.1',
         'whenbigg', 'alder7run', 'steveM49', 'dick_pountain', 'ryvre',
         'UniversityofNumenor', 'TPDavis', 'drkevorkian', 'bioethics']
print len(members)
i = 0
for member in members:
    i += 1
    print '%d of %d, %s' % (i, len(members), member)
    if member not in later:
        books.find_json_name(member)
