import books
import friends
import members
import json


def load_local_friends():
    """()->dict
    dsc: loads all friends list from file
    """
    result = {}
    with open('./data/friends.json', 'r') as name_repository:
        for line in name_repository:
            record = json.loads(line)
            result.update(record)
    return result


def all_local_members():
    """()->dict
    dsc: loads all members in friends file
    """
    result = []
    with open('./data/friends.json', 'r') as name_repository:
        for line in name_repository:
            record = json.loads(line)
            result.extend(record.keys())
            if record.values()[0].__class__ == list:
                result.extend(record.values()[0])
    result = list(set(result))
    return result


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
    print members
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
    #title = sys.argv[1]
    #work = books.get_work_title_retry(title)
    #members = members.find_all_members(work[:-1])
    #title = 'The Holy Bible: King James Version (KJV)'
    #title = 'The Blind Watchmaker'
    #title = 'Mere Christianity'
    #title = 'The Holy Bible: Revised Standard Version (RSV)'
    #title = 'The Holy Bible: New King James Version (NKJV)'
    #title = 'The Holy Bible: New American Standard (NASB)'
    #title = 'The God Delusion'
    #work = '1576656'
    #work = '306947'
    #work = '1595966'
    #work = '324481'
    #work = '5503022'
    #work = '5503098'
    #work = '1429542'
    #members = members.find_all_members(work)  # all members of given work
    known = load_local_friends()  # all known usernames
    #users = find_friends_bfs(members, known)
    #find_friends_recursive(members, known)
    all_members = all_local_members()
    find_missing_friends(all_members, known)
    #books.log('%s finished completely' % title)
