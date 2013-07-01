#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
All methods related to books in LT
"""
__all__ = ["find_all_members", "find_tags", "find_reviews"]

import json
from urllib2 import *
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from time import sleep
import re
from helpers import *
from users import find_json_name


def get_reviews(work):
    """(str)->list
    dsc: get all reviews of given book work id. result includes user name of
    reviewer, ranke he gave to work and the main text of the review
    """
    url = """http://www.librarything.com/ajax_profilereviews.php?offset=0
&type=3&showCount=10000&workid=%s&languagePick=en&mode=profile""" % work
    url = url.replace('\n', '')
    result = []
    try:
        html = urlopen(url)
        html = BeautifulSoup(html.read())
        reviews = html.findAll('div', attrs={'class': 'bookReview'})
        if reviews:
            for review in reviews:
                text = review.find('div', attrs={'class': 'commentText'}).text
                text = text.encode('utf-8')
                cntl_itm = review.find('span', attrs={'class': 'controlItems'})
                user = cntl_itm.find('a').text
                rv_lnk = review.find('span', attrs={'class': 'rating'})
                if rv_lnk:
                    rv_txt = rv_lnk.find('img')['src']
                    rank = re.search('ss(\d+).gif', rv_txt).group(1)
                else:
                    rank = 'NA'
                result.append({'name': user, 'text': text, 'rank': rank})
    except HTTPError, err:
        log("Error # "+str(err.code))
        return result
    except URLError, err:
        log(str(err.reason))
        return result
    return result


def find_reviews(work):
    """(str)->list
    dsc: get all reviews of given book work id if not exist in local storage
    >>>len(find_reviews('1060'))
    483
    """
    # if we have the information local
    with open('./data/books_review.json', 'r') as book_repository:
        for line in book_repository:
            record = json.loads(line)
            if work in record.keys():
                return record[work]
    with open('./data/books_review.json', 'a') as book_repository:
        review = get_reviews(work)
        if review != []:
            record = json.dumps({work: review})
            book_repository.write(record+'\n')
        else:
            log('no review found for work with id %s' % work, 'Error')
            return 'NA'
    return review


def get_members(work):
    """(str)->str
    dsc: returns a html string of a book memebers
    """
    print 'Retrieving data for %s...' % work
    url = "http://www.librarything.com/ajaxinc_userswithabook.php?work=" + work
    result = 'NA'
    try:
        html = urlopen(url)
        result = html.read()
        # save the result
        with open('./data/book/'+work+'.html', 'w') as data:
            data.write(result)
    except HTTPError, err:
        if err.code == 404:
            log("Page not found!", 'Error')
        elif err.code == 403:
            log("Access denied!", 'Error')
        else:
            log("Error "+str(err.code), 'Error')
    except URLError, err:
        log(str(err.reason), 'Error')
    return result


def find_all_members(work, rank='all'):
    """(str)->list
    dsc: find all members of a given book
    >>>len(find_all_members('306947'))
    4479
    >>>len(find_all_members('306947',  # no rank or more than 2 star
                            ['0', '4', '5', '6', '7', '8', '9', '10']))
    4441
    """
    result = []
    try:  # read content if file exits
        with open('./data/book/'+work+'.html') as f:
            data = f.read()
    except IOError:  # otherwise get it and save it  for further use
        data = get_members(work)
    data = BeautifulSoup(data)
    if rank == 'all':
        links = data.findAll('a')
        if links:
            for a in links:
                result.append(a['href'][9:])  # trim tags to get profile name
    else:
        links = []
        ranks = data.findAll('img')
        for i in rank:
            if i == '0':
                if data.find('b').text == 'No rating':
                        links.extend(data.find('b').findNextSiblings('a'))
            else:
                links.extend(ranks[-int(i)].findNextSiblings('a'))
        for a in links:
            result.append(a['href'][9:])  # trim tags to get profile name
    return result


def get_all_tag_work(work):
    """(str)->dic
    dsc: get all tags and counts for given book in a dictionary
    """
    url = """http://www.librarything.com/ajaxinc_showbooktags.php?work=%s
&all=1&print=1&doit=1&lang=en""" % work
    url = url.replace("\n", "")
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
    tags = html.findAll('span', attrs={'class': 'tag'})
    for tag in tags:
        name = tag.find('a').text
        count = tag.find('span', attrs={'class': 'count'}).text[1:-1]
        if name in result:
            log('tag %s from %s overwited' % (name, work))
        result.update({name: count})
    return result


def find_tags(work):
    """(str)->dict
    dsc: find all tags from local storage otherwise download and save it
    >>>find_tags('dummy')
    {'11111': '24', '22222': '1'}
    >>>len(find_tags('306947'))
    1701
    """
    # if we had the information local
    with open('./data/books_tags.json', 'r') as tag_repository:
        for line in tag_repository:
            record = json.loads(line)
            if work in record.keys():
                return record[work]
    #if we don't have tags for given work id
    tags = get_all_tag_work(work)
    if tags != {}:
        with open('./data/books_tags.json', 'a') as tag_repository:
            record = json.dumps({work: tags})
            tag_repository.write(record+'\n')
        return record
