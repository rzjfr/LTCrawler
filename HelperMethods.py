import json
from datetime import datetime


def log(message, types='Warning'):
    """(str)->None
    dsc: logging events to onebig file
    """
    date = str(datetime.now())
    with open("./LT.log", "a") as f:
        f.write(date+" "+message+"\n")
    print "%s: %s, more information in LT.log" % (types, message)


def load_local_friends(path='./data/friends.json'):
    """()->dict
    dsc: loads all friends list from file
    """
    result = {}
    with open(path, 'r') as name_repository:
        for line in name_repository:
            record = json.loads(line)
            result.update(record)
    return result


def all_local_members(path='./data/friends.json'):
    """()->dict
    dsc: loads all members in friends file
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
