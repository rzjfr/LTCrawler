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
    with open("./data/friends.log", "a") as file:
        file.write(date+" "+message+"\n")
    print("Error: "+message+", more information in book.log")


def get_all_friends(name):
    """(str)->list
    dsc: find all friends of a given person
    >>>get_all_friends('Jon.Roemer')
    ['Movielizard', 'Vintagecoats']
    >>>get_all_friends('masoodr')
    []
    """
    url = 'http://www.librarything.com/profile/' + quote(name)
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
    html = BeautifulSoup(html.read())
    result = []
    friends = html.find('div',
                        attrs={'class': 'profileactionsection first'})
    if not friends:
        log('no date for %s' % name)
    elif friends("p")[0].text == "No connections":
        return result
    else:
        for friend in friends('a'):
            result.append(friend.text)
    return result

print get_all_friends('masoodr')
