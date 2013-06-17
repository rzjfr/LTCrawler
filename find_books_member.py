import books
import json
from HelperMethods import *


members = load_local_friends()
for member in members:
    print member
    books.find_books(member)
