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


def get_all_tag_name(name):
    """(str)->dic
    dsc: get all tags and counts for given book
    """
    url = 'http://www.librarything.com/tagcloud.php?view=%s' % name
    try:
        html = urlopen(url)
        html = BeautifulSoup(html.read())
    except HTTPError, err:
        if err.code == 404:
            log("Page not found!", 'Error')
        elif err.code == 403:
            log("Access denied!", 'Error')
        else:
            log("Error "+str(err.code), 'Error')
    except URLError, err:
        log(str(err.reason), 'Error')
    result = {}
    tags_div = html.find('div', attrs={'class': 'tags'})
    tags = tags_div.findAll('span')
    for tag in tags:
        if tag.find('a'):
            tag_name = tag.find('a').text
            count = tag.find('span', attrs={'class': 'count'}).text[1:-1]
            if name in result:
                log('tag %s for %s overwited' % (tag_name, name))
            result.update({tag_name: count})
    return result


def find_all_tag_name(name):
    """(str)->dict
    dsc: find all tags from local storage otherwise download and save it
    >>>find_all_tag_work('dummy')
    {'11111': '24', '22222': '1'}
    """
    # if we had the information local
    with open('./data/tags_user.json', 'r') as tag_repository:
        for line in tag_repository:
            record = json.loads(line)
            if name in record.keys():
                return record[name]
    #if we don't have tags for given work id
    print 'Downloading tag list for %s' % name
    tags = get_all_tag_name(name)
    #if tags != {}:
    with open('./data/tags_user.json', 'a') as tag_repository:
        record = json.dumps({name: tags})
        tag_repository.write(record+'\n')
        return record

print find_all_tag_name('lissaleone')
print find_all_tag_name('jared_doherty')
print find_all_tag_name('MaryRose')
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
