# -*- coding: utf-8 -*-

import datetime
from sqlobject import *
import urllib

import BartleBlog.backend.config as config
import BartleBlog.backend.dbclasses as db

import BartleBlog.tools.yahoomenu
import BartleBlog.tools.addthis
import BartleBlog.tools.technorati
import BartleBlog.tools.yahoogrids
import BartleBlog.tools.yahoocalendar
import BartleBlog.tools.haloscan
import BartleBlog.tools.intensedebate
import BartleBlog.tools.disqus
import BartleBlog.tools.statcounter
import BartleBlog.tools.feedburner
import BartleBlog.tools.delicious
import BartleBlog.tools.mootools

class Macros:
    def __init__ (self,blog):
        self.blog=blog
        blog.macros=self
        self.head=[]

        self.yahooMenu=BartleBlog.tools.yahoomenu.factory(blog)
        self.addThis=BartleBlog.tools.addthis.factory(blog)
        self.technorati=BartleBlog.tools.technorati.factory(blog)
        self.yahooGrids=BartleBlog.tools.yahoogrids.factory(blog)
        self.yahooCalendar=BartleBlog.tools.yahoocalendar.factory(blog)
        self.haloScan=BartleBlog.tools.haloscan.factory(blog)
        self.statCounter=BartleBlog.tools.statcounter.factory(blog)
        self.feedBurner=BartleBlog.tools.feedburner.factory(blog)
        self.delicious=BartleBlog.tools.delicious.factory(blog)
        self.mootools=BartleBlog.tools.mootools.factory(blog)
        self.intensedebate=BartleBlog.tools.intensedebate.factory(blog)
        self.disqus=BartleBlog.tools.disqus.factory(blog)

    def chunk(self,name):
        s=db.Chunk.select(db.Chunk.q.name==name)
        if s.count():
            return s[0].text
        else:
            return ''
        
    def translationsBar(self):
        tl=db.Translation.select()
        if tl.count():
            s="""Available in: %s"""% \
            """<span class="meta-sep">|</span>""".join(['<span><a href="%s/weblog/index.html">%s</a></span>'\
                                                        %('/tr/'+t.code, t.name) for t in tl]+\
              ['<span><a href="%sweblog/index.html">%s</a></span>'%\
              ('/',config.getValue('blog', 'langname', 'English' ))])  
            return s
        return ""

    def translationsBarForPost(self, post):
        tl=post.translations()
        if tl:
            ms="""<span class="meta-sep">|</span>"""
            s="""Available in: %s"""% \
            ms.join(['<span><a href="%s">%s</a></span>'%(self.weblogPermaLink(post, t), t.name) for t in tl]+\
                ['<span><a href="%s">%s</a></span>'%(self.weblogPermaLink(post),config.getValue('blog', 'langname', 'English' ))])  
            return s
        return ""
        
    #################################################################################
    ### <head> manipulation
    #################################################################################

    def cleanHead(self):
        self.head=[]

    def addHead(self,headers):
        for h in headers:
            if not h in self.head:
                self.head.append(h)

    def insertHead(self):
        return '\n'.join(self.head)

    def rstHead(self):
        return [
        '<link rel="stylesheet" type="text/css" href="%s">'%self.absoluteUrl('static/css/rst.css'),
        '<link rel="stylesheet" type="text/css" href="%s">'%self.absoluteUrl('static/css/bartleblog.css'),
        '<link rel="stylesheet" type="text/css" href="%s">'%self.absoluteUrl('static/css/code.css'),
        '<link rel="stylesheet" type="text/css" href="%s">'%self.absoluteUrl('static/css/pygment/%s.css')%config.getValue('pygment','style','murphy')
        ]

    def catRssHead(self, cat):
        return ['<link rel="alternate" type="application/rss+xml" title="RSS for category %s" href="%s">'%(cat.name, self.absoluteUrl('categories/%s.xml'%cat.name.lower()))]

    #################################################################################
    ### General Macros
    #################################################################################

    def weblogPermaLink(self,post, lang=None):
        date=post.pubDate
        if isinstance(post, db.Post):
            if lang==None:
                return self.absoluteUrl(post.myurl())
            return self.absoluteUrl("tr/%s/weblog/posts/%s.html"%(lang.code,post.postID))
        elif isinstance(post, db.Story):
            if lang==None:
                return self.absoluteUrl("stories/%s.html"%(post.postID))
            return self.absoluteUrl("tr/%s/stories/%s.html"%(lang.code,post.postID))
        else:
            raise("Hell")

    def getUrlForDay(self,date, lang=None):
        if lang==None:
            return self.absoluteUrl("weblog/%s/%02d/%02d.html"%(date.year,date.month,date.day))
        return self.absoluteUrl("tr/%s/weblog/%s/%02d/%02d.html"%(lang,date.year,date.month,date.day))

    def absoluteUrl(self,path):
        return self.blog.basepath+path

    def copyright(self,rss=False):
        s=db.Post.select(orderBy=db.Post.q.pubDate)
        if s.count():
            earliest=db.Post.select(orderBy=db.Post.q.pubDate)[0].pubDate
        else:
            earliest=datetime.date.today()
        if rss:
            return u"Copyright %d-%d %s"%(earliest.year,datetime.date.today().year,self.blog.author)
        return u"&copy; %d-%d %s &lt;%s&gt;"%(earliest.year,datetime.date.today().year,self.blog.author,self.blog.author_email)
