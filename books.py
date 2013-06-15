import json
from urllib2 import *
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from time import sleep
import re
import mechanize


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
    title = title.encode('utf-8')
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


def get_shared_books(member_a, member_b):
    """(str, str)->str
    dsc: compares books for each member and returns number of same books
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
            log("Page not found!")
        elif err.code == 403:
            log("Access denied!")
        else:
            log("Error "+str(err.code))
    except URLError, err:
        log(str(err.reason))
    return 'NA'


def find_shared_books(user_a, user_b):
    """(str, str)->str
    dsc: compare # of same books for each user.find from local or get it online
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
        name_repository.write(record+'\n')
    return works


def find_shared_books_2(user_a, user_b, f):
    """(str, str, funcrion)->str
    find shared books of two users with given find books function
    """
    works_a = f(user_a)
    works_b = f(user_b)
    result = []
    for work in works_a:
        if work in works_b:
            result.append(work)
    return result


def get_books(name):
    """('str')->list
    get all unique works of given name from html page and save all in one file
    """
    user_agent = """Mozilla/5.0 (X11; U; Linux i686;
 en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1"""
    user_agent = user_agent.replace("\n", "")
    agent = mechanize.Browser()
    agent.addheaders = [('User-agent', user_agent)]
    url = 'http://www.librarything.com/catalog_bottom.php?view=%s' % name
    try:
        browser = agent.open(url)
    except HTTPError, err:
        log("Error "+str(err.code))
        return 'NA'
    except URLError, err:
        log(str(err.reason))
        return 'NA'
    repeat = True
    htmls = []
    books = []
    while repeat:
        htmls.append(browser.read())
        has_next_page = re.search('\>next page\<\/a\>', htmls[-1])
        books.extend(re.findall('/work/(\d+)/', htmls[-1]))
        i = re.search('(<td class="pbGroup">\d{1,7} &ndash; )(.{6,20})(</td>)'
                      , htmls[-1])
        if i is None:
            log('book list for %s is NA' % name)
            break
        print 'downloading %s for %s...' % (i.group(2), name)
        if has_next_page:
            offset = str(50*len(htmls))
            url = """http://www.librarything.com/catalog_bottom.php?
view=%s&offset=%s""" % (name, offset)
            url = url.replace("\n", "")
            sleep(0.5)
            try:
                browser = agent.open(url)
            except HTTPError, err:
                log("Error "+str(err.code))
                return 'NA'
            except URLError, err:
                log(str(err.reason))
                return 'NA'
        else:
            repeat = False
    print '%d pages crawled for %s' % (len(htmls), name)
    # save all pages in one file
    with open('./data/profile/html/%s.html' % name, 'w') as name_repository:
        content = '\n'.join(htmls)
        name_repository.write(content)
    return list(set(books))  # return unique set of works


def find_books(name):
    """('str')->list
    find all unique works of given name (version 2, from html)
    """
    try:  # make sure the file exist
        with open('./data/profile/html/'+name+'.html', 'r') as file:
            data = file.read()
        books = re.findall('/work/(\d+)/', data)
        books = list(set(books))
    except IOError:  # otherwise get it and save it  for further use
        books = get_books(name)
    return books


def get_reviews(work):
    """(str)->list
    dsc: get all reviews of given book work id
    """
    junk = ['!', '@', '#', '$', '%', '&', '*', '(', ')','--', '_ ', '...', '|',
            '+', '=', '.', ',', ':', '~', '<', '>', '\'', '\"', '\\', '{', '}',
            '[', ']', '\xe2\x80\x93', '\xe2\x80\x94', '\xc2\xab', '?', '/',
            '\xe2\x80\x9c', '\xe2\x80\x99', '\xe2\x80\x9d', '\xc2\xbb', '- ']
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
            log('no review found for work with id %s' % work)
            return 'NA'
    return review

#print find_reviews('1060')
#print len(find_shared_books_2('Des2', 'Jon.Roemer', find_books))
#print len(find_shared_books_2('scducharme', 'CatsLiteracy', find_work_isbn))
#print len(find_shared_books_2('scducharme', 'CatsLiteracy', find_books))
