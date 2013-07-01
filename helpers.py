#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Some general helper methods
"""
__all__ = ["all_local_members", "count_items", "find_key_by_value", "log",
           "find_null_friends", "has_duplicate", "load_local_friends",
           "remove_duplicate", "sort_dict", "write_to_file",
           "find_users_shared_books"]

import json
from datetime import datetime
from time import time, sleep


def log(message, types='Warning'):
    """(str)->None
    dsc: logging events to onebig file
    """
    date = str(datetime.now())
    with open("./LT.log", "a") as f:
        f.write(date+" "+message+"\n")
    print "%s: %s, more information in LT.log" % (types, message)


def load_local_friends(path='./data/users_friends.json'):
    """()->dict
    dsc: loads all friends list from file
    """
    result = {}
    with open(path, 'r') as name_repository:
        for line in name_repository:
            record = json.loads(line)
            result.update(record)
    return result


def all_local_members(path='./data/users_friends.json'):
    """()->list
    dsc: returns all user names in friends file
    """
    result = []
    with open(path, 'r') as name_repository:
        for line in name_repository:
            record = json.loads(line)
            result.extend(record.keys())
            if record.values()[0].__class__ == list:
                result.extend(record.values()[0])
    result = list(set(result))
    return result


def has_duplicate(friends):
    """(list)->bool
    dsc: to find out if we mixed conections of a member with friends
    >>>has_duplicated([1, 1, 3])
    True
    >>>has_duplicated([1, 2, 3])
    False
    """
    for i in xrange(len(friends)):
        if friends[i] in friends[i+1:]:
            return True
    return False


def remove_duplicate(all_members):
    """(list)->list
    dsc: remove all duplicated items from given list
    # if user name data is not already in database
    >>>remove_duplicate([2,2,3,3,6])
    [2, 3, 6]
    """
    return list(set(all_members))


def count_items(all_members, member):
    """(list, str)-> int
    dsc: find count of a member in all member list
    >>>count_items([2,2,3,3,6], 3)
    2
    """
    result = 0
    for item in all_members:
        if item == member:
            result += 1
    return result


def write_to_file(record, path='./new.json'):
    """(str)->None
    dsc: add line to exitsting file
    """
    with open(path, 'a') as f:
        f.write(record+'\n')


def find_key_by_value(user, dic):
    """(str, dict)->list
    find all user names that has a specific user as a friend
    """
    result = []
    for name, friends in dic.items():
        if friends.__class__ == list:
            if user in friends:
                result.append(name)
        else:
            if user == friends:
                result.append(name)
    return result


def find_null_friends(dic):
    """(dict)->list
    find all user names that has no friend list
    """
    result = []
    for name, friends in dic.items():
        if not friends:
            result.append(name)
    return result


def pretify_time(seconds):
    """(int)->str
    dsc: retruns output of f and prints how much time it took
    """
    s = seconds
    if s / 60 >= 60:
        print '%d\' %d\" %d' % (s / 3600, (s % 3600) / 60, (s % 3600) % 60)
    elif s / 60 >= 1:
        print '%d\" %d' % (s / 60, s % 60)
    else:
        print s
    return s


def sort_dict(dic):
    """(dict)->list
    dsc: returns a list of given dictionary keys sorted by its value
    """
    return list(sorted(dic, key=dic.__getitem__, reverse=True))


def find_users_shared_books(user_a, user_b, f):
    """(str, str, funcrion)->str
    dsc: find shared books of two users with arbitrary find book works function
    """
    works_a = f(user_a)
    works_b = f(user_b)
    result = []
    for work in works_a:
        if work in works_b:
            result.append(work)
    return result
