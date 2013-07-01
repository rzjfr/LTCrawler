import books
import users as friends
import re
import nltk
import csv
from nltk.corpus import wordnet
from helpers import *


def load_sentiment():
    """()->dic
    """
    fp = './data/AFINN-111.txt'
    result = {}
    dataReader = csv.reader(open(fp), dialect='excel-tab')
    for raw in dataReader:
        result.update(dict(zip(raw[0::2], raw[1::2])))
    return result


def reviews_text(all_reviews, types='work'):
    """(list)->str
    dsc: returns all given reviews in one big text documet
    """
    junk = ['!', '@', '#', '$', '%', '&', '*', '(', ')', '--', '_ ', '...',
            '+', '=', '.', ',', ':', '~', '<', '>', '\'', '\"', '\\', '{', '}',
            '[', ']', '\xe2\x80\x93', '\xe2\x80\x94', '\xc2\xab', '?', '/',
            '\xe2\x80\x9c', '\xe2\x80\x99', '\xe2\x80\x9d', '\xc2\xbb', '- ',
            ' -', ';', '|']
    text = ""
    for review in all_reviews:
        if types == 'work':
            text += review['text']
        else:
            text += review
    text = text.encode('utf-8')
    text = text.lower()
    for item in junk:
        text = text.replace(item, ' ')
    return text


def word_frequency(text):
    """(str)->dict
    dsc: from document finds most used words
    """
    words = text.split()
    words = remove_duplicate(words)
    common_words = ['due', 'you', 'the', 'for', 'and', 'have', 'has', 'too',
                    'very', 'ill', 'them', 'your', 'them', 'would', 'been',
                    'mine', 'there', 'were', 'ing', 'his', 'her', 'that',
                    'this', 'not', 'but', 'was', 'with', 'here', 'nor', 'out',
                    'per', 'are', 'than', 'ever', 'ain', 'est', 'any', 'more',
                    'most', 'some', 'much', 'all']
    # porter stemmer
    #stemmer = nltk.PorterStemmer()
    # clean non words
    cleaned_words = []
    for word in words:
        if len(word) > 2:
            if word not in common_words:
                #word = stemmer.stem(word)
                cleaned_words.append(word)
    words = list(set(cleaned_words))

    result = {}
    for word in words:
        count = len(re.findall(word, text))
        result.update({word: count})
    return result


def point_reviews(sentiment, words):
    """(dic, list)->dic
    """
    point = 0
    for word in words:
        if word in sentiment:
            point += float(sentiment[word])
    return point


def meaning_percent(words, data='data'):
    """(list, text)->int
    dsc: how many of given words are in dictionary
    """
    result = 0
    if len(words) == 0:
        print 'This user has no reviews'
        return 'NA'
    for word in words:
        if wordnet.synsets(word):
            result += 1
    result = (result / float(len(words))) * 100.0
    print '%d' % result + '%' + ' of %s are meaningful' % data
    return result


#work = '1060'
work = '306947'
#work = '1576656'
all_reviews = books.find_reviews(work)
text = reviews_text(all_reviews, 'work')
freq = word_frequency(text)
word = sort_dict(freq)
tags = books.find_tags(work)
#same = []
#find = {}
#for k, v in freq.items():
    #if k in tags:
        #same.append([k, tags[k], v])
        #find.update({k: (float(tags[k].replace(',', '')) + v) / 2.0})
#print sorted(find.iteritems(), key=lambda x: x[1], reverse=True)
#print len(word), len(tags), len(same)
#print point_reviews(sentiment, text.split())
#print point_reviews(sentiment, tags)
print 'work %s has %d tags, %d words in reviews' % (work, len(tags), len(word))
sentiment = load_sentiment()
meaning_percent(tags.keys(), 'tags')
meaning_percent(word[:10], 'words')

print '\n'

#name = 'Jon.Roemer'
#name = 'MaryRose'
#name = 'yangguy'
#name = 'jocelynandersen'
name = 'BrJohnDismas'
all_reviews = friends.find_reviews(name)
text = reviews_text(all_reviews, 'username')
freq = word_frequency(text)
word = sort_dict(freq)
tags = friends.find_tags(name)
print 'user %s has %d tags, %d words in reviews' % (name, len(tags), len(word))
meaning_percent(tags.keys(), 'tags')
meaning_percent(word[:10], 'words')
