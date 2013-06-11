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



