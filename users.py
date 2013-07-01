#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
All methods related to user in LT
"""
__all__ = ["find_tags", "find_authors", "find_friends", "find_reviews",
           "find_books", "find_json_name"]

import json
from urllib2 import *
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import mechanize
from time import sleep
from helpers import *


def get_json_name(name):
    """(str)->str
    dsc: returns json formated string for given user name.
    API Documentations:
    www.librarything.com/wiki/index.php/LibraryThing_JSON_Books_API
    """
    print 'Retrieving data for %s...' % name
    url = '''http://www.librarything.com/api_getdata.php?
userid=%s&tagList=0&showstructure=1&max=1000000&
reviewmax=10000000&showCollections=1&showReviews=1&showCollections=1
&showTags=1&responseType=json''' % name
    url = url.replace("\n", "")
    try:
        respond = urlopen(url)
    except HTTPError, err:
        if err.code == 404:
            log("Page not found!", 'Error')
        elif err.code == 403:
            log("Access denied!", 'Error')
        else:
            log("Error "+str(err.code), 'Error')
    except URLError, err:
        log(str(err.reason), 'Error')
    #except ContentTooShortError, err:
        #log('Content too short for %s' % name, 'Error')
        #print('Retring...')
        #return get_json_name(name)
    data = respond.read()
    return data


def find_json_name(name):
    """(str)->str
    dsc: finds json file for a given user name and returns it as json formated
    string
    """
    try:  # if the file already exists
        with open('./data/profile/json/'+name+'.json') as f:
            data = f.read()
    except IOError:  # otherwise get it and save it
        data = get_json_name(name)
        with open("./data/profile/json/"+name+".json", "w") as f:
            f.write(data)
    return data


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
    >>>find_friends('Movielizard')
    ['atimmons', 'Jon.Roemer', 'onemoreday', 'Vintagecoats']
    >>>find_friends('gothic_cowgirl')
    No access
    """
    with open('./data/users_friends.json', 'r') as name_repository:
        for line in name_repository:
            record = json.loads(line)
            if name in record.keys():
                return record[name]
    friends = get_all_friends(name)
    with open('./data/users_friends.json', 'a') as name_repository:
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


def find_tags(name):
    """(str)->dict
    dsc: find all tags from local storage otherwise download and save it
    >>>find_all_tag_work('dummy')
    {'11111': '24', '22222': '1'}
    """
    # if we had the information local
    with open('./data/users_tags.json', 'r') as tag_repository:
        for line in tag_repository:
            record = json.loads(line)
            if name in record.keys():
                return record[name]
    #if we don't have tags for given work id
    print 'Downloading tag list for %s' % name
    tags = get_all_tag_name(name)
    #if tags != {}:
    with open('./data/users_tags.json', 'a') as tag_repository:
        record = json.dumps({name: tags})
        tag_repository.write(record+'\n')
    return tags


def find_reviews(name):
    """(str)->list
    dsc: get all reviews of given book work id if not exist in local storage
    >>>len(find_reviews('Jon.Roemer'))
    15
    >>>find_tags('lissaleone')
    {'library book': '9', 'own': '2'}
    >>>find_tags('jared_doherty')
    {}
    """
    # if we have the information local
    data = find_json_name(name)
    result = []
    if data:
        data = json.loads(data)
        if 'books' in data.keys() and data['books']:
            for book_id in data['books'].keys():
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
    >>>len(remove_duplicate(find_authors('Jon.Roemer')))
    95
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


def get_books(name):
    """('str')->list
    dsc: get all unique works of given name from LT catalog html page and saves
    all in one file and returns unique book work ids for given user name
    """
    user_agent = """Mozilla/5.0 (X11; U; Linux i686;
 en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1"""
    user_agent = user_agent.replace("\n", "")
    agent = mechanize.Browser()
    agent.addheaders = [('User-agent', user_agent)]
    url = 'http://www.librarything.com/catalog_bottom.php?view=%s' % name
    try:
        browser = agent.open(url)
    except HTTPError, err:
        log("Error "+str(err.code))
        return 'NA'
    except URLError, err:
        log(str(err.reason))
        return 'NA'
    repeat = True
    htmls = []
    books = []
    while repeat:
        htmls.append(browser.read())
        has_next_page = re.search('\>next page\<\/a\>', htmls[-1])
        books.extend(re.findall('/work/(\d+)/', htmls[-1]))
        i = re.search('(<td class="pbGroup">\d{1,7} &ndash; )(.{6,20})(</td>)',
                      htmls[-1])
        if i is None:
            log('book list for %s is NA' % name)
            break
        print 'downloading %s for %s...' % (i.group(2), name)
        if has_next_page:
            offset = str(50*len(htmls))
            url = """http://www.librarything.com/catalog_bottom.php?
view=%s&offset=%s""" % (name, offset)
            url = url.replace("\n", "")
            #sleep(0.5)
            try:
                browser = agent.open(url)
            except HTTPError, err:
                log("Error "+str(err.code))
                return 'NA'
            except URLError, err:
                log(str(err.reason))
                return 'NA'
        else:
            repeat = False
    print '%d pages crawled for %s' % (len(htmls), name)
    # save all pages in one file
    with open('./data/profile/catalog/%s.html' % name, 'w') as name_repository:
        content = '\n'.join(htmls)
        name_repository.write(content)
    return remove_duplicate(books)


def find_books(name):
    """('str')->list
    dsc: finds all unique works of given name from LT catalog html page and
    saves all in one file and returns unique book work ids for given user name
    >>>len(find_books('Jon.Roemer'))
    141
    >>>len(set(find_books('cc_rec')))
    47
    """
    try:  # make sure the file exist
        with open('./data/profile/catalog/'+name+'.html', 'r') as file:
            data = file.read()
        books = re.findall('/work/(\d+)/', data)
        books = remove_duplicate(books)
    except IOError:  # otherwise get it and save it  for further use
        books = get_books(name)
    return books

get_user_page('the_red_shoes')
