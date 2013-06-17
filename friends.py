import json
from urllib2 import *
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from time import sleep
from HelperMethods import *


def get_all_friends(name):
    """(str)->list
    dsc: find all friends of a given person
    >>>get_all_friends('Jon.Roemer')
    ['Movielizard', 'Vintagecoats']
    >>>get_all_friends('masoodr')
    []
    """
    print 'Retrieving friends list for %s...' % name
    url = 'http://www.librarything.com/profile/' + quote(name)
    result = []
    friends = None  # to solve pass 403 error
    try:
        html = urlopen(url)
        html = BeautifulSoup(html.read())
        friends = html.find('div',
                            attrs={'class': 'profileactionsection first'})
    except HTTPError, err:
        if err.code == 404:
            log("Page not found!")
            return 'No access'
        elif err.code == 403:
            log("Access denied!")
            return 'No access'
        else:
            log("Error "+str(err.code))
            return 'No access'
    except URLError, err:
        log(str(err.reason))
        return 'No access'
    if not friends:
        alert = html.find('p', attrs={'class': 'alert'})
        profile = html.find('div', attrs={'class': 'profile'})
        if alert:
            log('No data for %s: %s' % (name, alert.text[:-1]))
            return 'Removed'
        elif profile:
            log('No data for %s: user data is private' % name)
            return 'Private'
        else:
            alert = html.find('p')
            if alert:
                msg = alert.text[22:-1]
                if msg == 'User has been deleted or never existed':
                    log('No data for %s: %s' % (name, msg))
                    return 'Not exist'
                else:
                    log('No data for %s: Unknown Problem' % name)
                    return 'NA'
    elif friends("p")[0].text == "No connections":
        log('No data for %s: No connection' % name)
        return 'No connection'
    else:
        if friends.find('p'):
            friends = friends.find('p')
        if friends.find('b').text == 'Friends:':
            for friend in friends('a'):
                result.append(friend.text)
        else:
            log('No data for %s: No list is available' % name)
            return 'No list'
    return result


def find_friends(name):
    """(str)->list
    dsc: find friends from local storage or get it from internet
    >>>find_friends('dummy')
    ['11111', '22222']
    >>>find_friends('masoodr')
    []
    """
    with open('./data/friends.json', 'r') as name_repository:
        for line in name_repository:
            record = json.loads(line)
            if name in record.keys():
                return record[name]
    friends = get_all_friends(name)
    with open('./data/friends.json', 'a') as name_repository:
        record = json.dumps({name: friends})
        name_repository.write(record+'\n')
    return friends

#print get_all_friends('Zaki_Jalil')
#print get_all_friends('Mysterion')
#print get_all_friends('razorsoccamsells')
#print get_all_friends('vchia')
#print get_all_friends('newsativa')
#print find_friends('Movielizard')
#print find_friends('gothic_cowgirl')
#print get_all_friends('CLHarris')
#print get_all_friends('aakin')
#print get_all_friends('DiannaN')
