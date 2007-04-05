# -*- coding: utf-8 -*-

import os,re,cgi,datetime
from sqlobject import *
from BartleBlog.util.html2text import html2text
import BartleBlog.rst as rst

class Category(SQLObject):
    name=UnicodeCol(alternateID=True)
    description=UnicodeCol()
    title=UnicodeCol()
    posts=RelatedJoin('Post',orderBy='pubDate')
    stories=RelatedJoin('Story',orderBy='pubDate')
    magicWords=UnicodeCol()
    def myurl(self):
        return "categories/%s.html"%(self.name.lower())

def fteaser (self):
    try:
        return cgi.escape(html2text(self.rendered)[:100])
    except:
        return cgi.escape(self.text[:100])
        
def frender (self):
    if self.structured:
        html,code=rst.rst2html(self.text)
        # FIXME notice RST errors
        self.rendered=html
        self.is_dirty=code
    else:
        self.rendered=self.text
        self.is_dirty=-1

def guessCategories(text):
    text=text.lower()
    res=[]
    for cat in Category.select():
        if not cat.magicWords:
            continue
        for word in cat.magicWords.split(' '):
            if re.compile(' %s |^%s | %s$'%(word,word,word)).findall(text): 
                res.append(cat.name)
                break
    return res
    
class Post(SQLObject):
    postID=UnicodeCol(alternateID=True)
    title=UnicodeCol()
    text=UnicodeCol()
    link=UnicodeCol(default='')
    source=UnicodeCol(default='')
    sourceUrl=UnicodeCol(default='')
    rendered=UnicodeCol(default='')
    onHome=BoolCol(default=True)
    structured=BoolCol(default=True)
    pubDate=DateTimeCol(default=datetime.datetime.now())
    categories=RelatedJoin('Category',orderBy='name')
    is_dirty=IntCol(default=-1)
    def myurl(self):
        return "weblog/%d/%02d/%02d.html#%s"%(self.pubDate.year,
                                                self.pubDate.month,
                                                self.pubDate.day,
                                                self.postID)
    teaser=fteaser
    render=frender


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
    is_dirty=IntCol(default=-1)
    link=None #Ok, this one is cheating
    categories=RelatedJoin('Category')
    def myurl(self):
        return "stories/%s.html"%self.postID
    teaser=fteaser
    render=frender
    link=''

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
