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

#print get_members_work('12569876')
