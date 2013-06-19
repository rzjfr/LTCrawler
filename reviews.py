import books
import re
import nltk
import csv
from nltk.corpus import wordnet
from HelperMethods import *


def load_sentiment():
    """()->dic
    """
    fp = './data/AFINN-111.txt'
    result = {}
    dataReader = csv.reader(open(fp), dialect='excel-tab')
    for raw in dataReader:
        result.update(dict(zip(raw[0::2], raw[1::2])))
    return result


def reviews_text(work):
    """(str)->str
    dsc: get all reviews in one big text documet
    """
    junk = ['!', '@', '#', '$', '%', '&', '*', '(', ')', '--', '_ ', '...',
            '+', '=', '.', ',', ':', '~', '<', '>', '\'', '\"', '\\', '{', '}',
            '[', ']', '\xe2\x80\x93', '\xe2\x80\x94', '\xc2\xab', '?', '/',
            '\xe2\x80\x9c', '\xe2\x80\x99', '\xe2\x80\x9d', '\xc2\xbb', '- ',
            ' -', ';', '|']
    all_reviews = books.find_reviews(work)
    text = ""
    for review in all_reviews:
        text += review['text']
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
    words = list(set(words))
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


def meaning_percent(words):
    """(list)->int
    dsc: how many of given words are in dictionary
    """
    result = 0
    for word in words:
        if wordnet.synsets(word):
            result += 1
    result = (result / float(len(words))) * 100.0
    print '%d' % result + '%'
    return result


text = reviews_text('1060')
freq = word_frequency(text)
word = list(sorted(freq, key=freq.__getitem__, reverse=True))
tags = books.find_all_tag_work('1060')
#same = []
#find = {}
#for k, v in freq.items():
    #if k in tags:
        #same.append([k, tags[k], v])
        #find.update({k: (float(tags[k].replace(',', '')) + v) / 2.0})
#print sorted(find.iteritems(), key=lambda x: x[1], reverse=True)
#print len(word), len(tags), len(same)

sentiment = load_sentiment()
print point_reviews(sentiment, text.split())
print point_reviews(sentiment, tags)
meaning_percent(tags)
meaning_percent(word[:10])
