"""
finds all friends list for all  given work id members and saves the results
in a json file: "./data/users_friends.json"
"""
import books
import users as friends
import json
import sys
from helpers import *


def find_missing_friends(members, known):
    """(list)->None
    dsc: find user names that no friend list is found for them
    """
    for member in members:
        if member not in known:
            all_friends = friends.find_friends(member)
            known.update({member: all_friends})
            find_friends_recursive(all_friends, known)


def find_friends_recursive(members, known):
    """(list)->None
    dsc: gets all members of a given book and returns friends
    for each one recursively
    """
    i = 0
    #print members
    if members.__class__ == list:
        for name in members:
            i += 1
            print '%d of %d' % (i, len(members))
            print "find friends for %s" % name
            all_friends = friends.find_friends(name)
            if all_friends.__class__ == list and all_friends:
                if name not in known:
                    print "continue with %s" % str(all_friends)
                    known.update({name: all_friends})
                    find_friends_recursive(all_friends, known)
            else:
                print 'done for %s' % name
        print "finished successfully! %d" % len(members)


def find_friends_bfs(members, known):
    """(list, dict)->list
    dsc: find first level of friends and return known stage
    """
    i = 0
    users_to_find_next = []
    if members.__class__ == list:
        for name in members:
            i += 1
            print '%d of %d, find friends for %s' % (i, len(members), name)
            all_friends = friends.find_friends(name)
            if all_friends.__class__ == list and all_friends:
                users_to_find_next.extend(all_friends)
    return list(set(users_to_find_next))

if __name__ == '__main__':
    #work = sys.argv[1]
    #work = books.get_work_title_retry(title)
    #members = books.find_all_members(work[:-1])
    #work = '1576656'  # The Blind Watchmaker
    #work = '306947'  # The Holy Bible: King James Version (KJV)
    #work = '1595966'  # Mere Christianity
    #work = '324481'  # The Holy Bible: Revised Standard Version (RSV)
    #work = '5503022'  # The Holy Bible: New King James Version (NKJV)
    #work = '5503098'  # The Holy Bible: New American Standard (NASB)
    #work = '1429542'  # The God Delusion
    #work = '34883'  # The End of Faith
    #work = '274277'  # The New English Bible; New Testament
    work = '2482940'  # God Is Not Great
    members = books.find_all_members(work)  # all members of given work
    known = load_local_friends()  # all known usernames
    #users = find_friends_bfs(members, known)
    find_friends_recursive(members, known)
    all_members = all_local_members()
    print 'finding friends for missing members...'
    known = load_local_friends()  # all known usernames
    find_missing_friends(all_members, known)
    books.log('work id %s finished completely' % work, 'Notification')
