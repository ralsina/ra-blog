# -*- coding: utf-8 -*-

import os
from sqlobject import *
import urllib

class Category(SQLObject):
    name=UnicodeCol(alternateID=True)
    posts=RelatedJoin('Post')
    stories=RelatedJoin('Story')

class Post(SQLObject):
    postID=UnicodeCol(alternateID=True)
    title=UnicodeCol()
    link=UnicodeCol()
    source=UnicodeCol()
    sourceUrl=UnicodeCol()
    text=UnicodeCol()
    rendered=UnicodeCol()
    onHome=BoolCol()
    structured=BoolCol()
    pubDate=DateTimeCol()
    categories=RelatedJoin('Category')
    def myurl(self):
        return u"http://lateral.blogsite.org/weblog/%d/%02d/%02d.html#%s"%(self.pubDate.year,
                                                                      self.pubDate.month,
                                                                      self.pubDate.day,
                                                                      self.postID)    
            
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
    categories=RelatedJoin('Category')
    def myurl(self):
        return "http://lateral.blogsite.org/stories/%s.html"%self.postID

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
