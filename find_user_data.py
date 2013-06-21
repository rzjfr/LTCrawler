import books
import json
import sys
from HelperMethods import *

try:
    work = sys.argv[1]
    #members = load_local_friends()
except:
    work = '306947'
members = books.find_all_members(work)  # all members of given work
members = remove_duplicate(members)
print len(members)
i = 0
for member in members:
    i += 1
    print '%d of %d, %s' % (i, len(members), member)
    if member != 'Kaethe':
        books.find_json_name(member)
