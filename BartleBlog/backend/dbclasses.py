# -*- coding: utf-8 -*-

import os,re,cgi,datetime
from sqlobject import *
from BartleBlog.util.html2text import html2text
import BartleBlog.rst as rst

def categoryByName(name):
    cq=Category.select(Category.q.name==name)
    if cq.count():
        return cq[0]
    return None

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
def postPreviewById(id):
    print id
    sq=PostPreview.select(PostPreview.q.postID==id)
    if sq.count():
        return sq[0]
    else:
        return None
        
def pageByPath(path):
    pq=Page.select(Page.q.path==path)
    if pq.count():
        p=pq[0]
    else:
        p=Page(path=path)
    return p
    
def translationByLangNamePost(lang, post):
    
    if isinstance (post, Post):
        tclass=TranslatedPost
    elif isinstance (post, Story):
        tclass=TranslatedStory
    else:
        raise ("Hell")
    
    trl=Translation.select(Translation.q.name==lang)
    if trl.count():
        t=trl[0]
        tpl=tclass.selectBy(lang=t, post=post)
        if tpl.count():
            return tpl[0]
        return tclass (lang=t, post=post, text=post.text, 
                              rendered=post.rendered, title=post.title, 
                              structured=post.structured )
    else:
        print "Error no translation to %s created"%lang
        return
        
def translationByLangCodePost(lang, post):
    if isinstance (post, Post):
        tclass=TranslatedPost
    elif isinstance (post, Story):
        tclass=TranslatedStory
    else:
        raise ("Hell")
    trl=Translation.select(Translation.q.code==lang)
    if trl.count():
        t=trl[0]
        tpl=tclass.selectBy(lang=t, post=post)
        if tpl.count():
            return tpl[0]
        return tclass(lang=t, post=post, text=post.text, 
                              rendered=post.rendered, title=post.title, 
                              structured=post.structured )
    else:
        print "Error no translation to %s created"%lang
        return


def fsetCategories(self,categories):

    # First mark as dirty those categories the post
    # doesn't belong anymore
    for c in self.categories:
        if not c in categories:
            c.setDirtyPages()
            self.removeCategory(c)

    # Now mark as dirty all the new categories
    # for the post
    for c in categories:
        if not c in self.categories:
            c.setDirtyPages()
            self.addCategory(c)


def fteaser (self):
    try:
        t=cgi.escape('\n\n'.join(html2text(self.rendered).split('\n\n')[:2]))
    except:
        t=cgi.escape(self.text)
      
#    if len(t)==250:  
#        l=t.split(' ')[:-1]
#        t=' '.join(l)
    return t

def frender (self):
    if self.structured:
        # Since this is to be embedded on HTML pages, start at H2
        # instead of H1
        try:
          html,code=rst.rst2html(self.text, settings_overrides= {'initial_header_level':2})
        except:
          print "ERROR rendering ",self.title
          html=''
          code=0 
        # FIXME notice RST errors
        self.rendered=html
        self.is_dirty=code
    else:
        self.rendered=self.text
        self.is_dirty=-1        
    self.modDate=datetime.datetime.now()

def matchesCategory(text, cat):
    res=False
    if cat.magicWords:
        for word in cat.magicWords.split(' '):
            if re.compile(' %s |^%s | %s$'%(word,word,word)).findall(text):
                res=True
                break
    return res
def guessCategories(text):
    text=text.lower()
    res=[]
    for cat in Category.select():
        if matchesCategory(text, cat):
            res.append(cat.name)
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
    def setDirtyPages(self):    
        '''Mark related pages as dirty'''    
        pages=[]
        pages.append('categories/index.html')
        pages.append('categories/%s.html'%(self.name))        
        for path in pages:
            p=pageByPath(path)
            p.is_dirty=True

class Translation(SQLObject):
    name=UnicodeCol()
    code=UnicodeCol()

class TranslatedPost(SQLObject):
    text=UnicodeCol(default='')
    rendered=UnicodeCol(default='')
    title=UnicodeCol(default='')
    lang=ForeignKey("Translation")
    post=ForeignKey("Post")
    structured=BoolCol(default=True)
    teaser=fteaser
    render=frender

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

    def translated(self, lang):
        if lang==None:
            return self
        return translationByLangCodePost(lang.code, self)
        

    def myurl(self, lang=None):
        if lang:
            return "tr/%s/weblog/%d/%02d/%02d.html#%s"%(lang.code,
                                                        self.pubDate.year,
                                                        self.pubDate.month,
                                                        self.pubDate.day,
                                                        self.postID)
            
        return "weblog/%d/%02d/%02d.html#%s"%(self.pubDate.year,
                                                self.pubDate.month,
                                                self.pubDate.day,
                                                self.postID)
    teaser=fteaser
    render=frender
    setCategories=fsetCategories
    def translations(self):
        return [ x.lang for x in TranslatedPost.selectBy(post=self)]

    def setDirtyPages(self):    
        '''Mark related pages as dirty'''
    
        post=self
        pages=[]
        pages.append('weblog/%s/index.html'%post.pubDate.year)
        pages.append('weblog/%s/%s/index.html'%(post.pubDate.year,post.pubDate.month))
        pages.append('weblog/%s/%s/%s.html'%(post.pubDate.year,post.pubDate.month,post.pubDate.day))
        pages.append('weblog/index.html')
            
        for c in post.categories:
            pages.append('categories/%s.html'%c.name.lower())
        if len(post.categories)>0:
            pages.append('categories/index.html')            
        
        for path in pages:
            p=pageByPath(path)
            p.is_dirty=True

class PostPreview(Post):
    categories=[]

class TranslatedStory(SQLObject):
    text=UnicodeCol(default='')
    rendered=UnicodeCol(default='')
    desc=UnicodeCol(default='')
    title=UnicodeCol(default='')
    lang=ForeignKey("Translation")
    post=ForeignKey("Post")
    structured=BoolCol(default=True)
    teaser=fteaser
    render=frender

class Story(SQLObject):
    postID=UnicodeCol(alternateID=True)
    title=UnicodeCol()
    desc=UnicodeCol(default='')
    text=UnicodeCol()
    rendered=UnicodeCol(default='')
    structured=BoolCol(default=True)
    draft=BoolCol(default=False)
    quiet=BoolCol(default=False)
    is_dirty=IntCol(default=-1)
    categories=RelatedJoin('Category')
#    pages=RelatedJoin('Page')
    def translations(self):
        return [ x.lang for x in TranslatedStory.selectBy(post=self)]
    def translated(self, lang):
        if lang==None:
            return self
        return translationByLangCodePost(lang.code, self)

    is_dirty=IntCol(default=-1)

    pubDate=DateTimeCol(default=datetime.datetime.now())
    modDate=DateTimeCol(default=datetime.datetime.now())

    def myurl(self, lang=None):
        if lang:
            return "tr/%s/stories/%s.html"%(lang.code, self.postID)
        return "stories/%s.html"%self.postID
    def teaser(self):
        if  self.desc:
            return self.desc
        else:
            return ""    
    render=frender
    setCategories=fsetCategories
    link=''
    def setDirtyPages(self):    
        '''Mark related pages as dirty'''    
        post=self
        pages=[]
        pages.append('stories/%s.html'%post.postID)
        pages.append('stories/index.html')
        for c in post.categories:
            pages.append('categories/%s.html'%c.name.lower())
        if len(post.categories)>0:
            pages.append('categories/index.html')                    
        for path in pages:
            p=pageByPath(path)
            p.is_dirty=True

class Chunk(SQLObject):
    name=UnicodeCol(alternateID=True)
    text=UnicodeCol(default='')
            
def initDB(name):
    #Initialize sqlobject
    db_fname=os.path.abspath(name)
    connection_string='sqlite:'+db_fname
    connection=connectionForURI(connection_string)
    sqlhub.processConnection = connection
    
    for t in [ Translation, TranslatedPost, TranslatedStory, Post, PostPreview, Story, Category, Page, Chunk ]:
        try:
            t.createTable()
        except dberrors.OperationalError:
            pass
        
        
