# -*- coding: utf-8 -*-

import os,re,cgi,datetime
from sqlobject import *
from BartleBlog.util.html2text import html2text
import BartleBlog.rst as rst

def categoryByName(name):
    cq=Category.select(Category.q.name==name)
    if cq.count():
        return cq[0]
    else:
        return Category(name=name,
                        description='Posts about %s'%name,
                        title='Posts about %s'%name)
                        
def storyById(id):
    sq=Story.select(Story.q.postID==id)
    if sq.count():
        return sq[0]
    else:
        return None

def postById(id):
    sq=Post.select(Post.q.postID==id)
    if sq.count():
        return sq[0]
    else:
        return None

def fsetCategories(self,categories):

    # First mark as dirty those categories the post
    # doesn't belong anymore
    for c in self.categories:
        if not c in categories:
            c.is_dirty=99
            self.removeCategory(c)

    # Now mark as dirty all the new categories
    # for the post
    for c in categories:
        if not c in self.categories:
            c.is_dirty=99
            self.addCategory(c)


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
    self.modDate=datetime.datetime.now()

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
    
class Page(SQLObject):
    path=UnicodeCol(alternateID=True)
    is_dirty=BoolCol(default=True)
    

class Category(SQLObject):
    name=UnicodeCol(alternateID=True)
    description=UnicodeCol()
    title=UnicodeCol()
    posts=RelatedJoin('Post',orderBy='pubDate')
    stories=RelatedJoin('Story',orderBy='pubDate')
    magicWords=UnicodeCol(default='')
    is_dirty=IntCol(default=-1)
    def myurl(self):
        return "categories/%s.html"%(self.name.lower())


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
    categories=RelatedJoin('Category',orderBy='name')

    is_dirty=IntCol(default=-1)

    pubDate=DateTimeCol(default=datetime.datetime.now())
    modDate=DateTimeCol(default=datetime.datetime.now())

    def myurl(self):
        return "weblog/%d/%02d/%02d.html#%s"%(self.pubDate.year,
                                                self.pubDate.month,
                                                self.pubDate.day,
                                                self.postID)
    teaser=fteaser
    render=frender
    setCategories=fsetCategories

    def setDirty(self):    
        '''Mark related pages as dirty'''
    
        post=self
        pages=[]
        pages.append('weblog/%s/index.html'%post.pubDate.year)
        pages.append('weblog/%s/%s/index.html'%(post.pubDate.year,post.pubDate.month))
        pages.append('weblog/%s/%s/%s.html'%(post.pubDate.year,post.pubDate.month,post.pubDate.day))
        for c in post.categories:
            pages.append('categories/%s.html'%c.name.lower())
        if len(post.categories)>0:
            pages.append('categories/index.html')            
        pages.append('weblog/index.html')
        
        for path in pages:
            pq=Page.select(Page.q.path==path)
            if pq.count():
                p=pq[0]
            else:
                p=Page(path=path)
            p.is_dirty=True

class Story(SQLObject):
    postID=UnicodeCol(alternateID=True)
    title=UnicodeCol()
    desc=UnicodeCol()
    text=UnicodeCol()
    rendered=UnicodeCol()
    structured=BoolCol()
    draft=BoolCol()
    quiet=BoolCol()
    is_dirty=IntCol(default=-1)
    categories=RelatedJoin('Category')
    pages=RelatedJoin('Page')

    is_dirty=IntCol(default=-1)

    pubDate=DateTimeCol(default=datetime.datetime.now())
    modDate=DateTimeCol(default=datetime.datetime.now())

    def myurl(self):
        return "stories/%s.html"%self.postID
    teaser=fteaser
    render=frender
    setCategories=fsetCategories
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
        Page.createTable()