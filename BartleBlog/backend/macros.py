# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import datetime
from sqlobject import *
import urllib

import BartleBlog.backend.dbclasses as db
import BartleBlog.tools.yahoomenu
import BartleBlog.tools.addthis
import BartleBlog.tools.technorati
import BartleBlog.tools.yahoogrids
import BartleBlog.tools.yahoocalendar
import BartleBlog.tools.haloscan
import BartleBlog.tools.statcounter
import BartleBlog.tools.feedburner
import BartleBlog.tools.talkr
import BartleBlog.tools.delicious

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
        self.talkr=BartleBlog.tools.talkr.factory(blog)
        self.delicious=BartleBlog.tools.delicious.factory(blog)

    def absoluteUrl(self,path):
        return basepath+path


    #################################################################################
    ### <head> manipulation
    #################################################################################

    def addHead(self,headers):
        global head
        for h in headers:
            if not h in self.head:
                self.head.append(h)

    def insertHead(self):
        return '\n'.join(self.head)

    def rstHead(self):
        return [
        '<link rel="stylesheet" type="text/css" href="%s">'%self.absoluteUrl('static/css/rst.css'),
        '<link rel="stylesheet" type="text/css" href="%s">'%self.absoluteUrl('static/css/html.css'),
        '<link rel="stylesheet" type="text/css" href="%s">'%self.absoluteUrl('static/css/bartleblog.css'),
        '<link rel="stylesheet" type="text/css" href="%s">'%self.absoluteUrl('static/css/silvercity.css')
        ]

    #################################################################################
    ### General Macros
    #################################################################################

    def weblogPermaLink(self,post):
        date=post.pubDate
        return self.absoluteUrl("weblog/%s/%02d/%02d.html#%s"%(date.year,date.month,date.day,post.postID))

    def getUrlForDay(self,date):
        return self.absoluteUrl("weblog/%s/%02d/%02d.html"%(date.year,date.month,date.day))

    def absoluteUrl(self,path):
        return self.blog.basepath+path

    def copyright(self,rss=False):
        earliest=db.Post.select(orderBy=db.Post.q.pubDate)[0].pubDate
        if rss:
            return u"Copyright %d-%d %s"%(earliest.year,datetime.date.today().year,self.blog.author)
        return u"&copy; %d-%d %s &lt;%s&gt;"%(earliest.year,datetime.date.today().year,self.blog.author,self.blog.author_email)



    chunk={
    'blurb':u'''
    All contents of this site written by me are free.
    Copy, modify, whatever., just put my name in it, and if you change the contents,
    clearly say so in the same page. Please provide a link back to the original.

    '''
    }
