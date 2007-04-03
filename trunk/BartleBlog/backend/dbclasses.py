# -*- coding: utf-8 -*-

import os
from sqlobject import *
import urllib
from BartleBlog.util.html2text import html2text
import BartleBlog.rst as rst
import cgi,datetime

class Category(SQLObject):
    name=UnicodeCol(alternateID=True)
    description=UnicodeCol()
    title=UnicodeCol()
    posts=RelatedJoin('Post',orderBy='pubDate')
    stories=RelatedJoin('Story',orderBy='pubDate')
    def myurl(self):
        return "categories/%s.html"%(self.name.lower())

def fteaser (self):
    try:
        return cgi.escape(html2text(self.rendered)[:100])
    except:
        return cgi.escape(self.text[:100])
        
def frender (self):
    pass

class Post(SQLObject):
    postID=UnicodeCol(alternateID=True)
    title=UnicodeCol()
    text=UnicodeCol()
    link=UnicodeCol(default=None)
    source=UnicodeCol(default=None)
    sourceUrl=UnicodeCol(default=None)
    rendered=UnicodeCol(default=None)
    onHome=BoolCol(default=True)
    structured=BoolCol(default=True)
    pubDate=DateTimeCol(default=datetime.datetime.now())
    categories=RelatedJoin('Category',orderBy='name')
    is_dirty=BoolCol(default=True)
    def myurl(self):
        return "weblog/%d/%02d/%02d.html#%s"%(self.pubDate.year,
                                                self.pubDate.month,
                                                self.pubDate.day,
                                                self.postID)
    teaser=fteaser


class Story(SQLObject):
    postID=UnicodeCol(alternateID=True)
    pubDate=DateTimeCol()
    title=UnicodeCol()
    desc=UnicodeCol()
    text=UnicodeCol()
    rendered=UnicodeCol()
    structured=BoolCol()
    draft=BoolCol()
    quiet=BoolCol()
    link=None #Ok, this one is cheating
    categories=RelatedJoin('Category')
    def myurl(self):
        return "stories/%s.html"%self.postID
    teaser=fteaser

def initDB(name):
    #Initialize sqlobject
    db_fname=os.path.abspath(name)
    connection_string='sqlite:'+db_fname
    connection=connectionForURI(connection_string)
    sqlhub.processConnection = connection

    if not os.path.exists(db_fname):
        Post.createTable()
        Story.createTable()
        Category.createTable()
