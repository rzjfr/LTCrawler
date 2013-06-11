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
    with open("./data/tags.log", "a") as file:
        file.write(date+" "+message+"\n")
    print("Error: "+message+", more information in tags.log")


def get_all(work):
    """(str)->dic
    dsc: get all tags and counts for given book
    """
    url = """http://www.librarything.com/ajaxinc_showbooktags.php?work=%s
&all=1&print=1&doit=1&lang=en""" % work
    url = url.replace("\n", "")
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
    result = {}
    tags = html.findAll('span', attrs={'class': 'tag'})
    for tag in tags:
        name = tag.find('a').text
        count = tag.find('span', attrs={'class': 'count'}).text[1:-1]
        if name in result:
            log('tag %s from %s overwited' % (name, work))
        result.update({name: count})
    return result


print get_all('306947')
