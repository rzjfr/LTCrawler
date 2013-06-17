import json
from urllib2 import *
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from time import sleep
from HelperMethods import *


def get_all_tag_work(work):
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
            log("Page not found!", 'Error')
        elif err.code == 403:
            log("Access denied!", 'Error')
        else:
            log("Error "+str(err.code), 'Error')
    except URLError, err:
        log(str(err.reason), 'Error')
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


#print find_all_tag_work('306947')
#print find_all_tag_work('dummy')
