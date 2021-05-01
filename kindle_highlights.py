import sys
import os
import re

# these variables must be updated to work
src = "your kindle location here"
dst = "your note taking folder here"

highlight_separator = "=========="


def parse_highlight(raw_highlight) :

    splitted_string = raw_highlight.split("\n")
    # parse author and title from first line of text (splitted_string[0] is empty)
    match = re.search(r'.+?(?= \((.*?)\))',splitted_string[1])

    if not match:
        return None, None, None, None
    
    print("date line: " + splitted_string[2])
    date = splitted_string[2]
    if splitted_string[4] == "":
        return None, None, None, None
    # the content is stored on the 4th line of text
    content = splitted_string[4]   
    
    title = match.group(0)
    if title.find(':') != -1 :
        title = title.split(':')[0]

    author= []
    author.append(match.group(1))
    if author[0].find(';') != -1 :
        author = author[0].split(';')

    return author, title, date, content

# a particular highlight from a particular book    
class Highlight:

    # the constructor in python, must be passed 'self' as an argument
    def __init__(self, raw_highlight):
        
        (self.author,
        self.title,
        self.date,
        self.content,) = parse_highlight(raw_highlight)

# a collection of highlights from a particular book
class Book:
    # list of all books in library
    book_list = set()
    
    def __init__ (self, title, author) :
        self.title = title
        self.author = author
        self.tags = []
        self.content = []
        Book.book_list.add(self.title)

    def add_tag(self, tag) :
        self.tags.append(tag)

    def add_author(self, author) :
        self.author.append(author)

    def add_highlight(self, highlight, date) :
        
        self.content.append(highlight + "\n" + date)
    
    def print_Highlights(self) :
        for highlight in self.content:
            print(highlight + "\n")

    def write_book(self) :
        clean_title = self.title.replace("\ufeff", "")
        file_name = ""+dst + "/" + clean_title + ".md"
        if self.title == None or len(self.content) == 0 :
            return False
        for entry in os.scandir(dst) :
            with open(file_name, "w+", encoding='utf-8-sig') as f :
                f.write(" # "+ clean_title + " \n ")
                for a in self.author :
                    f.write("Author: [[" + a + "]] \n")

                if self.tags != None :
                    f.write("Tags: ")
                    for t in self.tags :
                        f.write("#" + t + " ")
                f.write("\n")
                for h in self.content :
                    f.write("#### " + h + "\n")
                    f.write("\n")

if os.path.exists(src) :
    with open(src, "r", encoding='utf-8-sig') as f :
        data = f.read()
        highlight_list = data.split((highlight_separator))
        library = []
        for i in highlight_list:
            # parse raw highlight into formatted highlight
            h = Highlight(i)
            if h.title != None and h.author != None and h.content != None:
                # check if book is already in library
                if h.title not in Book.book_list :
                    # add new book to library
                    b = Book(h.title,h.author)
                    b.add_highlight(h.content, h.date)
                    b.add_tag("books")
                    library.append(b)
                else :
                    # find matching book in library and add new content
                    for b in library :
                        if b.title == h.title :
                            b.add_highlight(h.content, h.date)
        f.close()
            # now that the library has been filled with books, and books filled with content, we can write new content to the appropriate location (dst)
        if os.path.exists(dst) :
            for book in library :
                print(book.title+ "\n")
                print(len(book.content))
                book.write_book()
else :
    print("cannot find 'My Clippings': check if kindle is connected")
    
