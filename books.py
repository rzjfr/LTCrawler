import json
from urllib2 import *
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from time import sleep
import re


def log(message):
    """(str)->None
    dsc: logging
    """
    date = str(datetime.now())
    with open("./data/book.log", "a") as file:
        file.write(date+" "+message+"\n")
    print("Error: "+message+", more information in book.log")


def get_isbn_title(title):
    """(str)->str
    dsc: find isbn from given title
    >>>get_isbn_title('Information Cloud (Tales of Cinnamon City)')
    0957219008
    """
    print 'Retrieving isbn for %s...' % title
    url = 'http://www.librarything.com/api/thingTitle/'
    try:
        xml = urlopen(url+title)
    except HTTPError, err:
        if err.code == 404:
            log("Page not found!")
        elif err.code == 403:
            log("Access denied!")
        else:
            log("Error "+str(err.code))
    except URLError, err:
        log(str(err.reason))
    xml = BeautifulSoup(xml.read())
    if xml.find('isbn'):
        return xml.find('isbn').text
    else:
        log('No isbn found for '+str(title))
        return get_work_title_retry(title)


def get_work_title_retry(title):
    """(str)->str
    dsc: find work from given title if not found from isbn
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
            log("Page not found!")
        elif err.code == 403:
            log("Access denied!")
        else:
            log("Error "+str(err.code))
    except URLError, err:
        log(str(err.reason))
    xml = BeautifulSoup(xml.read())
    if xml.find('item'):
        return xml.find('item')['id']+'W'  # add 'W' to ditinguish from isbn
    else:
        log('Even after retry no isbn found for '+str(title))
        return 'NA'


def get_json_name(name):
    """(str)->str
    dsc: find json file for given name
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
            log("Page not found!")
        elif err.code == 403:
            log("Access denied!")
        else:
            log("Error "+str(err.code))
    except URLError, err:
        log(str(err.reason))
    data = respond.read()
    return data


def find_isbn_name(name):
    """(srt) -> list
    dsc: return all isbn list of a given person
    >>>find_isbn_name("sds")
    []
    """
    try:  # make sure the file exist
        with open('./data/profile/'+name+'.json') as file:
            data = file.read()
    except IOError:  # otherwise get it and save it  for further use
        data = get_json_name(name)
        with open("./data/profile/"+name+".json", "w") as file:
            file.write(data)
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
            log("Page not found!")
        elif err.code == 403:
            log("Access denied!")
        else:
            log("Error "+str(err.code))
    except URLError, err:
        log(str(err.reason))
    xml = BeautifulSoup(xml.read())
    if xml.find('work'):
        return xml.find('work').text
    else:
        log('No work id for %s' % isbn)
        return 'NA'


def get_compare_book(member_a, member_b):
    """(str, str)->int
    dsc: compares books for each member and returns number of same books
    >>>get_compare_book('Des2', 'Jon.Roemer')
    43
    """
    print 'Retrieving data to compare %s and %s...' % (member_a, member_b)
    base = 'http://www.librarything.com/'
    url = 'catalog_bottom.php?view=%s&compare=%s' % (member_a, member_b)
    print base+url
    try:
        html = urlopen(base+url)
        html = BeautifulSoup(html.read())
        if html.find('td', attrs={'class': 'pbGroup'}):
            text = html.find('td', attrs={'class': 'pbGroup'}).text
            if re.search('(?<=of) \d*', text):
                return re.search('(?<=of) \d*', text).group(0)[1:]
    except HTTPError, err:
        if err.code == 404:
            log("Page not found!")
        elif err.code == 403:
            log("Access denied!")
        else:
            log("Error "+str(err.code))
    except URLError, err:
        log(str(err.reason))
    return 'NA'


def find_work_isbn(name):
    """(str)->dict
    dsc: returns a list of books workid for given member
    >>>find_isbn_name('dum')
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
        name_repository.write(record)
    return works

#print find_isbn_name('Jon.Roemer')
#print find_work_isbn('Jon.Roemer')
#print get_compare_book('Des2', 'Jon.Roemer')
