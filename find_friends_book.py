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
            if record.values() != []:
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
    for name in members:
        print "find friends for %s" % name
        all_friends = friends.find_friends(name)
        if all_friends != []:
            if name not in known:
                print "continue with %s" % str(all_friends)
                known.update({name: all_friends})
                find_friends_recursive(all_friends, known)
            #else:
                #for friend in all_friends:
                    #if friend not in known:
                        #found_friends = friends.find_friends(friend)
                        #known.update({friend: found_friends})
                        #find_friends_recursive(found_friends, known)
        else:
            print 'done for %s' % name
    print "finished successfully!"


if __name__ == '__main__':
    #title = sys.argv[1]
    title = 'The Holy Bible: King James Version (KJV)'
    work = books.get_work_title_retry(title)
    members = members.find_all_members(work[:-1])
    known = load_local_friends()  # all known usernames
    find_friends_recursive(members, known)
    all_members = all_local_members()
    find_missing_friends(all_members, known)
    books.log('%s finished completely' % title)
