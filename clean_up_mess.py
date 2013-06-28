import json
import ast
import users as f
from helpers import *


def string_to_json():
    """
    dsc: just to correct saving utf strings instead of real json format
    """
    with open('./new_friends.json.bak', 'r') as member_repository:
        for line in member_repository:
            record = line.rstrip()
            record = ast.literal_eval(record)
            record = json.dumps(record)
            write_to_new(record)


def probably_wrong():
    """()->list
    dsc: find users that we probably found friends for them by mistake
    """
    result = []
    with open('./friends.json.bak2', 'r') as member_repository:
        for line in member_repository:
            record = json.loads(line)
            name = record.keys()[0]
            friends = record.values()[0]
            if friends == []:
                if count_items(all_members, name) > 1:
                    result.append(name)
    names = []
    for name in result:
        members = find_value_by_key(name)
        names.extend(members)
    names = remove_duplicate(names)
    return names
    #print len(result)


def find_null_friends():
    """()->list
    find all user names that has no friend list
    """
    result = []
    with open('./friends.json', 'r') as member_repository:
        for line in member_repository:
            record = json.loads(line)
            name = record.keys()[0]
            friends = record.values()[0]
            if not friends:
                result.append(name)
    return result


def redownload_null_friends(null_friends):
    """(list)->None
    dsc: unusual to have empty friend list.
    """
    for name in null_friends:
        friends = f.get_all_friends(name)
        with open('./friends.json', 'a') as name_repository:
            record = json.dumps({name: friends})
            print record
            name_repository.write(record+'\n')


def remove_null_friends():
    """"""
    with open('./friends.json', 'r') as member_repository:
        for line in member_repository:
            record = json.loads(line)
            friends = record.values()[0]
            if friends:
                write_to_new(line)


#remove_null_friends()
#null_friends = find_null_friends()
#redownload_null_friends(null_friends)
#print null_friends

#all_members = all_local_members()
#clean_data_base(all_members)
#print find_value_by_key('jiffykodak')
#print count_items(all_members, 'amercer')
#print len(probably_wrong())
