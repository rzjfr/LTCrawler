import books
import users
import json
import sys
from helpers import *

all_members = all_local_members()
print len(all_members)
i = 0
for name in all_members:
    i += 1
    print '%f%s done, %s' % ((i/float(len(all_members))), '%', name)
    users.get_user_page(name)
