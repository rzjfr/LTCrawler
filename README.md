LT Crawler
===========================
crawler for getting information from [LT](www.Librarything.com)


## Modules
  * **books.py**: all methods for finding data for given book
  * **users.py**: all methods for finding data for given username
  * **helpers.py**: some general and helper methods

## Scripts
  * **find_books_users.py**: find books for list of members with book ids in json data from [LT JSON API](http://www.librarything.com/wiki/index.php/LibraryThing_JSON_Books_API)
  * **find_books_users_html.py**: find books for list of members with LT Catalogs for each member
  * **find_friends_book.py**: find friends for members of a book
  * **find_user_data.py**: get all json data from LT JSON API for all members of a given book
  * **graph_friends.py**: graph analysis for members of two different books
  * **reviews.py**: text analysis for reviews by book or user
  * **xml_work_to_isbn.py**: to add isbn to work record from [LT feed files](http://www.librarything.com/feeds/)
  * **clean_up_mess.py**: to clean the data sets if something goes wrong

## Folders
  * **data/backup/**: all backup files
  * **data/book/**: members page of book with work id in html format
  * **data/feeds/**: LT files
  * **data/profile/**: all information of member in json format from [LT JSON API](http://www.librarything.com/wiki/index.php/LibraryThing_JSON_Books_API)
  * **data/profile/html/**: all books of each member in html format
  * **figures**: all figures including charts graphs in PDF, PNG and SVG formats

## Data Sets
###friends.json
each line a username with her friends username list

    {"CorkyRingspot": ["loubyloo", "wordhound"]}

`*_members.json` files contain friends list for members of only one book

###books.json
each line a username with its book work id list

    {"username": ["workid", "workid"]}

###book_review.json
each line work id with list of reviews. Each review contains text, username and rank

    {"workid": [{"text": "...", "name": "username", "rank": "2"}, {...}]}

###tags.json
each line work id with tags. Each tag contains tag text as key and frequency as value

    {"1060": {"read": "42", "fic": "2", "print book": "1"}}

`tags_user.json` is similar to `tags.json` but it contains tags for users

###isbn_to_work.csv
each line isbn with its corresponding work id

    isbn,workid
    002901986,483379

###bookid.csv
each line book id with its corresponding work id

    bookid,workid
    86408774,111247

###Other files
  * **compare.csv**: number of shared books between to members

    ``username,username,#of_shared_books``

  * **AFINN-111.text**: tsv format file, english words with sentiment rank for them at each line
  * **english.stop**: list of english stop words at each line

##URIs
* **Members List**: http://www.librarything.com/ajaxinc_userswithabook.php?work=306947
* **Books Catalog**: http://www.librarything.com/catalog_bottom.php?view=Des2&compare=Jon.Roemer

      Parameters: `view, compare, tag, ddc, offset, viewstyle`

* **Member Tags**: http://www.librarything.com/tagcloud.php?view=EmScape
* **Book Tags**: http://www.librarything.com/ajaxinc_showbooktags.php?work=306947&all=1&print=1&doit=1&lang=en
* **Author Cloud**: http://www.librarything.com/profile_sharedfavorites.php?view=hornakfinn
* **Reviews**: http://www.librarything.com/ajax_profilereviews.php?offset=0&type=3&showCount=10000000&workid=1060&languagePick=en&mode=profile
* **JSON API**: http://www.librarything.com/api_getdata.php?userid=masoodr&tagList=0&showstructure=1&max=100000&showReviews=0&showCollections=0&showTags=1&responseType=json
* **Friends List**: http://www.librarything.com/profile/rzjfr
* **Feeds data sets**: http://www.librarything.com/feeds

#TODO
## Data preparation
  * make a work to ISBN dataset
  * find friends of a given user
  * find books of a given user
  * find tags of a work, user
  * find reviews of a work, user
  * find authors of a user
  * find members of a work

## Analysis
  *  compare members of two books
  *  analysing reviews of the books, users
