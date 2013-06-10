import json
from urllib2 import *


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
        print 'Not found in database, Retrieving information...'
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
        with open("./data/profile/"+name+".json", "w") as file:
            file.write(data)
    result = []
    data = json.loads(data)
    print data['books']['88174801']
    for book_id in data['books'].keys():
        result.append(data['books'][book_id]['ISBN_cleaned'])
    return result

print find_isbn_name("Jon.Roemer")
