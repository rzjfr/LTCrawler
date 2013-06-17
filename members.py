import json
from urllib2 import *
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from time import sleep
from HelperMethods import *


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


def find_all_members(work):
    """(str)->list
    dsc: find all members of a given book
    """
    try:  # read content if file exits
        with open('./data/book/'+work+'.html') as f:
            data = f.read()
    except IOError:  # otherwise get it and save it  for further use
        data = get_members_work(work)
    data = BeautifulSoup(data)
    links = data.findAll('a')
    result = []
    if links:
        for a in links:
            result.append(a['href'][9:])  # trim achor tags to get profile name
    return result

#print len(find_all_members('306947'))
