# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import datetime
import dbclasses as db
from sqlobject import *
import urllib

import modules.yahoomenu
import modules.addthis
import modules.technorati
import modules.yahoogrids
import modules.yahoocalendar
import modules.haloscan
import modules.statcounter
import modules.feedburner
import modules.talkr
import modules.delicious

class Macros:
    def __init__ (self,blog):
        self.blog=blog
        blog.macros=self
        self.head=[]

        self.yahooMenu=modules.yahoomenu.factory(blog)
        self.addThis=modules.addthis.factory(blog)
        self.technorati=modules.technorati.factory(blog)
        self.yahooGrids=modules.yahoogrids.factory(blog)
        self.yahooCalendar=modules.yahoocalendar.factory(blog)
        self.haloScan=modules.haloscan.factory(blog)
        self.statCounter=modules.statcounter.factory(blog)
        self.feedBurner=modules.feedburner.factory(blog)
        self.talkr=modules.talkr.factory(blog)
        self.delicious=modules.delicious.factory(blog)

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
        return u"&copy; %d-%d %s <%s>"%(earliest.year,datetime.date.today().year,self.blog.author,self.blog.author_email)



    chunk={
    'blurb':u'''
    All contents of this site written by me are free.
    Copy, modify, whatever., just put my name in it, and if you change the contents,
    clearly say so in the same page. Please provide a link back to the original.

    '''
    }