import json
from urllib2 import *
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from time import sleep


def log(message):
    """(str)->None
    dsc: logging
    """
    date = str(datetime.now())
    with open("./data/members.log", "a") as file:
        file.write(date+" "+message+"\n")
    print("Error: "+message+", more information in book.log")


def get_members_work(work):
    """(str)->str
    dsc: returns a html string of a book memebers
    """
    print 'Retrieving data for %s...' % work
    url = "http://www.librarything.com/ajaxinc_userswithabook.php?work=" + work
    try:
        html = urlopen(url)
    except HTTPError, err:
        if err.code == 404:
            log("Page not found!")
        elif err.code == 403:
            log("Access denied!")
        else:
            log("Error "+str(err.code))
    except URLError, err:
        log(str(err.reason))
    result = html.read()
    # save the result
    with open('./data/book/'+work+'.html', 'w') as data:
        data.write(result)
    return result


def find_all_members(work):
    """(str)->list
    dsc: find all members of a given book
    """
    try:  # read content if file exits
        with open('./data/book/'+work+'.html') as file:
            data = file.read()
    except IOError:  # otherwise get it and save it  for further use
        data = get_members_work(work)
    data = BeautifulSoup(data)
    links = data.findAll('a')
    result = []
    if links != []:
        for a in links:
            result.append(a['href'][9:])  # trim achor tags to get profile name
    return result

#print find_all_members('12569876')
