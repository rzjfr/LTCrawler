import json
from urllib2 import *
from BeautifulSoup import BeautifulSoup


def find_isbn_title(title):
    """(str)->str
    dsc: find isbn from given title
    >>>find_isbn_title('Information Cloud (Tales of Cinnamon City)')
    0957219008
    """
    url = 'http://www.librarything.com/api/thingTitle/'
    xml = urlopen(url+title).read()
    xml = BeautifulSoup(xml)
    if xml.find('isbn'):
        return xml.find('isbn').text
    else:
        return ''


def find_json_name(name):
    """(str)->str
    dsc: find json file for given name
    """
    url = '''http://www.librarything.com/api_getdata.php?
userid=%s&tagList=0&showstructure=1&max=1000000&
reviewmax=10000000&showCollections=1&showReviews=1&showCollections=1
&showTags=1&responseType=json''' % name
    url = url.replace("\n", "")
    try:
        respond = urlopen(url)
    except HTTPError, err:
        if err.code == 404:
            print "Page not found!"
        elif err.code == 403:
            print "Access denied!"
        else:
            print "Error ", err.code
    except URLError, err:
        print err.reason
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
        print 'Retrieving data for %s...' % name
        data = find_json_name(name)
        with open("./data/profile/"+name+".json", "w") as file:
            file.write(data)
    result = []
    if data:
        data = json.loads(data)
        if 'books' in data.keys():
            for book_id in data['books'].keys():
                isbn = data['books'][book_id]['ISBN_cleaned']
                if isbn == '':
                    title = data['books'][book_id]['title']
                    print 'Retrieving isbn for %s...' % title
                    isbn = find_isbn_title(title)
                    result.append(isbn)
                else:
                    result.append(isbn)
        return result
    else:
        return 'No data found for %s' % name

print find_isbn_name("Jon.Roemer")
#title = 'Information Cloud (Tales of Cinnamon City)'
#print find_isbn_title(title)
