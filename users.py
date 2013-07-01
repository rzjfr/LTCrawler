#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
All methods related to user in LT
"""
__all__ = ["find_all_tag_name", "find_authors", "find_friends", "find_reviews"]

import json
from urllib2 import *
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from time import sleep
from helpers import *
from books import find_json_name


def get_user_page(name):
    """(str)->str
    dsc: get profile page for given username and save it in html
    >>>len(get_user_page('masoodr'))
    15879
    >>>len(get_user_page('gothic_cowgirl'))
    9
    """
    try:  # read content if file already exits
        with open('./data/profile/page/'+name+'.html') as f:
            html = f.read()
    except IOError:  # otherwise get it and save it  for further use
        print 'Retrieving profile page for %s...' % name
        url = 'http://www.librarything.com/profile/' + quote(name)
        try:
            html = urlopen(url)
            html = html.read()
        except HTTPError, err:
            if err.code == 404:
                log("Page not found!", 'Error')
                html = 'No access'
            elif err.code == 403:
                log("Access denied!", 'Error')
                html = 'No access'
            else:
                log("Error "+str(err.code), 'Error')
                html = 'No access'
        except URLError, err:
            log(str(err.reason))
            html = 'No access'
        # save in file
        with open('./data/profile/page/%s.html' % name, 'w') as f:
            f.write(html)
    return html


def get_all_friends(name):
    """(str)->list
    dsc: find all friends of a given person
    >>>get_all_friends('Jon.Roemer')
    ['Movielizard', 'Vintagecoats']
    >>>get_all_friends('masoodr')
    No connection
    >>>get_all_friends('gothic_cowgirl')
    No access
    """
    result = []
    html = get_user_page(name)
    if html == 'No access':
        return html
    html = BeautifulSoup(html)
    friends = html.find('div',
                        attrs={'class': 'profileactionsection first'})
    if not friends:
        alert = html.find('p', attrs={'class': 'alert'})
        profile = html.find('div', attrs={'class': 'profile'})
        if alert:
            log('No data for %s: %s' % (name, alert.text[:-1]), 'Warning')
            return 'Removed'
        elif profile:
            log('No data for %s: user data is private' % name, 'Warning')
            return 'Private'
        else:
            alert = html.find('p')
            if alert:
                msg = alert.text[22:-1]
                if msg == 'User has been deleted or never existed':
                    log('No data for %s: %s' % (name, msg), 'Warning')
                    return 'Not exist'
                else:
                    log('No data for %s: Unknown Problem' % name, 'Error')
                    return 'NA'
    elif friends("p")[0].text == "No connections":
        # no friends list no intrested library means no connection
        return 'No connection'
    else:
        if friends.find('p'):
            friends = friends.find('p')
        if friends.find('b').text == 'Friends:':
            for friend in friends('a'):
                result.append(friend.text)
        else:
            # no friend list
            return 'No list'
    return result


def find_friends(name):
    """(str)->list
    dsc: returns friends list for given name
    >>>find_friends('dummy')
    ['11111', '22222']
    >>>find_friends('masoodr')
    No connection
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
    return tags


def find_reviews(name):
    """(str)->list
    dsc: get all reviews of given book work id if not exist in local storage
    """
    # if we have the information local
    data = find_json_name(name)
    result = []
    if data:
        data = json.loads(data)
        if 'books' in data.keys() and data['books']:
            for book_id in data['books'].keys():
                    #result.append(book_id)
                if data['books'][book_id]['hasreview'] == '1':
                    result.append(data['books'][book_id]['bookreview'])
        else:
            log('No review found for %s' % name, 'Warning')
        return result
    else:
        log('No data is available for %s' % name, 'Error')
    return result


def find_authors(name):
    """(str)->list
    dsc: from given user name returns all authors using json data file
    >>>find_authors('rzjfr')
    ['adamsdouglas']
    """
    data = find_json_name(name)
    result = []
    if data:
        data = json.loads(data)
        if 'books' in data.keys() and data['books']:
            for book_id in data['books'].keys():
                if data['books'][book_id]['author_code']:
                    result.append(data['books'][book_id]['author_code'])
        else:
            log('No books found for %s' % name, 'Error')
        return result
    else:
        log('No data is available for %s' % name, 'Error')
    return result


#print len(remove_duplicate(find_authors('Jon.Roemer')))
#print len(find_authors('Jon.Roemer'))
#print find_reviews('Jon.Roemer')
#print find_all_tag_name('lissaleone')
#print find_all_tag_name('jared_doherty')
#print find_all_tag_name('MaryRose')
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
