#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
All methods related to books in LT
"""
__all__ = ["find_all_members", "find_all_tag_work", "find_bookids_name",
           "find_isbn_name", "find_reviews", "find_shared_books",
           "find_shared_books_2", "find_work_isbn", "find_work_name"]

import json
from urllib2 import *
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from time import sleep
import re
from helpers import *
from users import find_json_name


def get_isbn_title(title):
    """(str)->str
    dsc: find isbn from given title
    >>>get_isbn_title('Information Cloud (Tales of Cinnamon City)')
    0957219008
    """
    print 'Retrieving isbn for %s...' % title
    url = 'http://www.librarything.com/api/thingTitle/'
    title = title.encode('utf-8')
    try:
        xml = urlopen(url+title)
    except HTTPError, err:
        if err.code == 404:
            log("Page not found!", 'Error')
        elif err.code == 403:
            log("Access denied!", 'Error')
        else:
            log("Error "+str(err.code), 'Error')
    except URLError, err:
        log(str(err.reason), 'Error')
    xml = BeautifulSoup(xml.read())
    if xml.find('isbn'):
        return xml.find('isbn').text
    else:
        log('No isbn found for '+str(title))
        return get_work_title_retry(title)


def get_work_title_retry(title):
    """(str)->str
    dsc: find workid from given title
    >>>get_work_title_retry('Freckle Juice')[:-1]
    '17'
    """
    print 'Retrieving isbn for %s...' % title
    key = 'ba4a76cea44a763da0317089b6b4c103'
    url = """http://www.librarything.com/services/rest/1.1/
?method=librarything.ck.getwork&name=%s&apikey=%s""" % (quote(title), key)
    url = url.replace("\n", "")
    try:
        xml = urlopen(url)
    except HTTPError, err:
        if err.code == 404:
            log("Page not found!", 'Error')
        elif err.code == 403:
            log("Access denied!", 'Error')
        else:
            log("Error "+str(err.code), 'Error')
    except URLError, err:
        log(str(err.reason), 'Error')
    xml = BeautifulSoup(xml.read())
    if xml.find('item'):
        return xml.find('item')['id']+'W'  # add 'W' to ditinguish from isbn
    else:
        log('Even after retry no isbn found for '+str(title))
        return 'NA'


def find_isbn_name(name):
    """(srt) -> list
    dsc: return all isbn list of a given user name (with duplicates)
    >>>find_isbn_name("sds")
    []
    >>>find_isbn_name("rzjfr")
    ['0345453743']
    """
    data = find_json_name(name)
    result = []
    if data:
        data = json.loads(data)
        if 'books' in data.keys() and data['books']:
            for book_id in data['books'].keys():
                isbn = data['books'][book_id]['ISBN_cleaned']
                if isbn == '':  # find missing isbn
                    title = data['books'][book_id]['title']
                    sleep(1)
                    isbn = get_isbn_title(title)
                    result.append(isbn)
                else:
                    result.append(isbn)
        else:
            message = 'No book found for %s' % name
            log(message)
        return result
    else:
        message = 'No data found for %s' % name
        log(message)


def find_bookids_name(name):
    """(srt) -> list
    dsc: gets all book ids of given user name from json data
    >>>find_bookids_name('rzjfr')
    ['97711987']
    """
    data = find_json_name(name)
    result = []
    if data:
        data = json.loads(data)
        if 'books' in data.keys() and data['books']:
            for book_id in data['books'].keys():
                    result.append(book_id)
        else:
            log('No data found for %s' % name, 'Error')
        return result
    else:
        log('No data found for %s' % name, 'Error')


def get_work_bookid(bookid):
    """(str)->str
    dsc: find work id for given book id
    >>>get_work_bookid('97711987')
    '9440376'
    """
    print 'Retrieving data for book with id: %s...' % bookid
    url = 'http://www.librarything.com/work/book/%s' % bookid
    #result = 'NA'
    try:
        html = urlopen(url)
        html = html.read()
        result = re.search('\/work\/(\d+)\/book\/', html).group(1)
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


def find_work_bookid(bookid):
    """(str)->str
    dsc: find work id for given book id from repository file or online
    >>>find_work_bookid('97711987')
    '9440376'
    """
    with open('./data/bookid.csv', 'r') as book_repository:
        for line in book_repository:
            record = line.rstrip()
            record = record.split(',')
            if record[0] == bookid:
                return record[1]
    # we don't have it, get it from website
    work = get_work_bookid(bookid)
    with open('data/bookid.csv', 'a') as book_repository:
        record = ','.join([bookid, work+'\n'])
        book_repository.write(record)
    return work


def find_work_name(name):
    """(str)->list
    dsc: find all works of a member with find_bookids_name method
    >>>find_work_name('rzjfr')
    ['9440376']
    """
    result = []
    bookids = find_bookids_name(name)
    i = 0
    if bookids:
        for bookid in bookids:
            i += 1
            print '%d of %d for %s' % (i, len(bookids), name)
            work = find_work_bookid(bookid)
            result.append(work)
    else:
        log('No data found for %s' % name, 'Error')
    return result


def get_work_isbn(isbn):
    """(str)->str
    dsc: find work id for given isbn
    >>>get_work_isbn('0957219008')
    12569876
    """
    print 'Retrieving data for %s...' % isbn
    base = 'http://www.librarything.com/'
    try:
        xml = urlopen(base+"api/whatwork.php?isbn="+isbn)
    except HTTPError, err:
        if err.code == 404:
            log("Page not found!", 'Error')
        elif err.code == 403:
            log("Access denied!", 'Error')
        else:
            log("Error "+str(err.code), 'Error')
    except URLError, err:
        log(str(err.reason), 'Error')
    xml = BeautifulSoup(xml.read())
    if xml.find('work'):
        return xml.find('work').text
    else:
        log('No work id for %s' % isbn)
        return 'NA'


def get_shared_books(member_a, member_b):
    """(str, str)->str
    dsc: get numbers of shared books for between two users using LT catalog
    >>>get_shared_books('Des2', 'Jon.Roemer')
    43
    """
    print 'Retrieving data to compare %s and %s...' % (member_a, member_b)
    base = 'http://www.librarything.com/'
    url = 'catalog_bottom.php?view=%s&compare=%s' % (member_a, member_b)
    try:
        html = urlopen(base+url)
        html = BeautifulSoup(html.read())
        if html.find('td', attrs={'class': 'pbGroup'}):
            text = html.find('td', attrs={'class': 'pbGroup'}).text
            if re.search('(?<=of) \d*', text):
                return re.search('(?<=of) \d*', text).group(0)[1:]
    except HTTPError, err:
        if err.code == 404:
            log("Page not found!", 'Error')
        elif err.code == 403:
            log("Access denied!", 'Error')
        else:
            log("Error "+str(err.code), 'Error')
    except URLError, err:
        log(str(err.reason), 'Error')
    return 'NA'


def find_shared_books(user_a, user_b):
    """(str, str)->str
    dsc: finds numbers of shared books for between two users using LT catalog
    >>>find_shared_books('Des2', 'Jon.Roemer')
    43
    """
    # if we have the information on disk
    with open('./data/compare.csv', 'r') as name_repository:
        for line in name_repository:
            record = line.rstrip()
            record = record.split(',')
            a = record[0]
            b = record[1]
            count = record[2]
            right_order = user_a == a and user_b == b
            misplaced = user_a == b and user_b == a
            if right_order or misplaced:
                return count
    # we don't have it, get it from website
    count = get_shared_books(user_a, user_b)
    if count == 'NA':  # retry one more time
        count = get_shared_books(user_a, user_b)

    with open('data/compare.csv', 'a') as name_repository:
        record = ','.join([user_a, user_b, count+'\n'])
        name_repository.write(record)
    return count


def find_work_isbn(name):
    """(str)->list
    dsc: returns a list of workid for given user name
    >>>find_isbn_name('rzjfr')
    ['0345453743']
    """
    # if we had the information local
    with open('./data/books.json', 'r') as name_repository:
        for line in name_repository:
            record = json.loads(line)
            if name in record.keys():
                return record[name]
    # if user name data is not already in database
    isbns = find_isbn_name(name)
    works = []
    found = ['NA']  # keep track of found isbns
    if isbns != []:
        # if we already have work id information for isbn
        for isbn in isbns:
            isbn_repository = open('./data/isbn_to_work.csv', 'r')
            for line in isbn_repository.readlines():
                if isbn == line.split(",")[0]:
                    works.append(line.split(",")[1].rstrip())
                    found.append(isbn)
            isbn_repository.close()
    isbns = [n for n in isbns if n not in found]  # remove found items
    isbn_repository = open('./data/isbn_to_work.csv', 'a')
    #if we don't have work id for isbn
    if isbns != []:
        for isbn in isbns:
            if isbn[-1] == 'W':
                work = isbn[:-1]
                works.append(work)
                found.append(isbn)
            elif isbn != 'NA':
                sleep(1)
                work = get_work_isbn(isbn)
                if work != 'NA':
                    works.append(work)
                    found.append(isbn)
                    isbn_repository.write(",".join([isbn, work+"\n"]))
    isbns = [n for n in isbns if n not in found]  # remove found items
    if isbns != []:
        log("we finished with work id missing for %s" % str(isbns))
    isbn_repository.close()
    with open('./data/books.json', 'a') as name_repository:
        record = json.dumps({name: works})
        name_repository.write(record+'\n')
    return works


def find_work_name_2(name):
    """(str)->list
    dsc: returns a list of workid for given user name
    """
    # if we had the information local
    with open('./data/books.json', 'r') as name_repository:
        for line in name_repository:
            record = json.loads(line)
            if name in record.keys():
                return record[name]
    # calculate it
    data = find_json_name(name)
    data = json.loads(data)
    isbns = []
    works = []
    if 'books' in data.keys() and data['books']:
        for book_id in data['books'].keys():
            isbn = data['books'][book_id]['ISBN_cleaned']
            if isbn == '':  # find missing isbn
                print '...'
                work = find_work_bookid(book_id)
                works.append(work)
            else:  # find work id
                isbns.append(isbn)
    else:
        message = 'No book found for %s' % name
        log(message)
    works.extend(find_isbn_work(isbns))
    return works


def find_isbn_work(isbns):
    """(list)->list
    dsc: from a list of isbns returns a list of works
    """
    base = "http://www.librarything.com/api/json/workinfo.js?ids="
    url = base + ','.join(isbns)
    try:
        html = urlopen(url)
        html = html.read()
        works = re.findall('(work\":\")(\d+)', html)
        works = [j for i, j in works]
        if len(works) != len(set(isbns)):
            log('Some isbns missing', 'Error')
        #else:  # no reason for this part
            #temp = zip(isbns,works)
            #for isbn, work in temp:
                #with open('./data/isbn_to_work.csv', 'a') as isbn_repository:
                    #isbn_repository.write(",".join([isbn, work+"\n"]))
        return works
    except HTTPError, err:
        if err.code == 404:
            log("Page not found!", 'Error')
        elif err.code == 403:
            log("Access denied!", 'Error')
        else:
            log("Error "+str(err.code), 'Error')
    except URLError, err:
        log(str(err.reason), 'Error')


def find_shared_books_2(user_a, user_b, f):
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
    """
    # if we have the information local
    with open('./data/book_review.json', 'r') as book_repository:
        for line in book_repository:
            record = json.loads(line)
            if work in record.keys():
                return record[work]
    with open('./data/book_review.json', 'a') as book_repository:
        review = get_reviews(work)
        if review != []:
            record = json.dumps({work: review})
            book_repository.write(record+'\n')
        else:
            log('no review found for work with id %s' % work, 'Error')
            return 'NA'
    return review


def get_members_work(work):
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
    """
    result = []
    try:  # read content if file exits
        with open('./data/book/'+work+'.html') as f:
            data = f.read()
    except IOError:  # otherwise get it and save it  for further use
        data = get_members_work(work)
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


def find_all_tag_work(work):
    """(str)->dict
    dsc: find all tags from local storage otherwise download and save it
    >>>find_all_tag_work('dummy')
    {'11111': '24', '22222': '1'}
    """
    # if we had the information local
    with open('./data/tags.json', 'r') as tag_repository:
        for line in tag_repository:
            record = json.loads(line)
            if work in record.keys():
                return record[work]
    #if we don't have tags for given work id
    tags = get_all_tag_work(work)
    if tags != {}:
        with open('./data/tags.json', 'a') as tag_repository:
            record = json.dumps({work: tags})
            tag_repository.write(record+'\n')
        return record

#print find_reviews('1060')
#print find_all_members('306947',  # find only with no rank or more than 1 star
                       #['0', '3', '4', '5', '6', '7', '8', '9', '10'])
#print len(find_shared_books_2('Des2', 'Jon.Roemer', find_books))
#print len(find_shared_books_2('scducharme', 'CatsLiteracy', find_work_isbn))
#print len(find_shared_books_2('scducharme', 'CatsLiteracy', find_books))
#print len(find_all_members('306947'))
#print find_all_tag_work('306947')
#print find_all_tag_work('dummy')
#print len(remove_duplicate(find_work_name('scducharme')))
#print len(remove_duplicate(find_work_name('CatsLiteracy')))
#print find_work_bookid('85886431')
#print find_work_bookid('71999056')
#print len(find_work_name_2('cc_rec'))
#print len(remove_duplicate(find_work_name('Jon.Roemer')))
