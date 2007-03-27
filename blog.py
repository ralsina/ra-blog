# -*- coding: utf-8 -*-

import os,sys
from dbclasses import *
import datetime
from cherrytemplate import renderTemplate
import codecs
import macros
import slimmer

class Blog:
    def __init__(self):
        db_fname=os.path.abspath('blog.db')
        connection_string='sqlite:'+db_fname
        connection=connectionForURI(connection_string)
        sqlhub.processConnection = connection
        self.dest_dir=os.path.abspath("weblog")
        self.blog_title="Lateral Opinion"
        
    def loadTemplate(self,name):
        fname=os.path.abspath('templates/%s.tmpl'%name)
        f=codecs.open(fname,"r","utf-8")
        return f.read()

    def renderBlogPage(self,title,curDate,itemtmpl,pagetmpl,dname,fname,postlist=None,story=None,body=None):
        # Render
        if body or body=="":
            pass
        else:
            body=renderTemplate(self.loadTemplate(itemtmpl))
            
        if pagetmpl:
            page=renderTemplate(self.loadTemplate(pagetmpl))
        else:
            page=body
        page=slimmer.html_slimmer(page)
        # Save or return
        if not fname:
            return page
        if not os.path.exists(dname):
            os.makedirs(dname)
        if os.path.exists(fname):
            os.unlink(fname)
        f=codecs.open(os.path.join(dname,fname),"w","utf-8")
        f.write(page)
             
    def renderStoryIndex(self):
        story_dir=os.path.join(self.dest_dir,'stories')        
        fname="index.html"
        postlist=Story.select(orderBy=Story.q.pubDate)
        title="%s - Story Index"%self.blog_title
        curDate=datetime.datetime.today()
        self.renderBlogPage(
                title,
                curDate,
                'storyIndex',
                'pageSite',
                story_dir,
                fname,
                postlist=postlist
            )
        
        
    def renderStories(self):
    
        self.renderStoryIndex()
    
        # Render stories
        story_dir=os.path.join(self.dest_dir,'stories')        
        for story in Story.select():
            title=story.title
            curDate=story.pubDate
            fname="%s.html"%(story.postID)
            self.renderBlogPage(
                    title,
                    curDate,
                    'storySite',
                    'pageSite',
                    story_dir,
                    fname,
                    story=story
                )
                
    
    def renderBlogIndex(self):
        postlist=list(Post.select(orderBy=Post.q.pubDate)[-20:])
        postlist.reverse()
        curDate=postlist[0].pubDate
        title=self.blog_title
        dname=os.path.join(self.dest_dir,"weblog")
        fname="index.html"
        
        self.renderBlogPage(
                title,
                curDate,
                'blogSite',
                'pageSite',
                dname,
                fname,
                postlist=postlist
            )
    
    def renderBlogDay(self,date):
        start=date.replace(hour=0,minute=0,second=0)
        end=date+datetime.timedelta(1)
        postlist=Post.select(AND(Post.q.pubDate>=start,Post.q.pubDate<end))
        if postlist.count()==0:
            return

        postlist=list(postlist)
        postlist.reverse()

        # Variables used by the templates
        title=self.blog_title
        curDate=postlist[0].pubDate
        dname=os.path.join(self.dest_dir,"weblog/%d/%02d"%(date.year,date.month))
        fname="%02d.html"%(date.day)
        
        self.renderBlogPage(
                title,
                curDate,
                'blogSite',
                'pageSite',
                dname,
                fname,
                postlist=postlist
            )
            
    def renderBlogMonth(self,date):
        start=date.replace(day=1,hour=0,minute=0,second=0)
        end=start
        if start.month==12:
            end=end.replace(year=start.year+1,day=1,month=1)
        else:
            end=end.replace(month=start.month+1)
        
        postlist=Post.select(AND(Post.q.pubDate>=start,Post.q.pubDate<end),
                                orderBy=Post.q.pubDate)
        if postlist.count()==0:
            return

        postlist=list(postlist)
        postlist.reverse()
        
        # Variables used by the templates
        title=self.blog_title
        curDate=postlist[0].pubDate
        dname=os.path.join(self.dest_dir,"weblog/%d/%02d"%(date.year,date.month))
        fname="index.html"
            
        self.renderBlogPage(
                title,
                curDate,
                'blogSite',
                'pageSite',
                dname,
                fname,
                postlist=postlist
            )

        for day in range(1,32):
            try:
                self.renderBlogDay(curDate.replace(day=day))
            except ValueError:
                #To avoid checking month length
                pass

    def renderBlogYear(self,year):
        for month in range(1,13):
            self.renderBlogMonth(datetime.datetime(year=year,month=month,day=1))
            
        # Yearly archive page
        start=datetime.datetime(year=year,day=1,month=1)
        contents=""
        for month in range(1,13):
            start=start.replace(day=1,month=month,hour=0,minute=0,second=0)
            end=start
            if start.month==12:
                end=end.replace(year=start.year+1,day=1,month=1)
            else:
                end=end.replace(month=start.month+1)
                
            postlist=Post.select(AND(Post.q.pubDate>=start,Post.q.pubDate<end),
                                orderBy=Post.q.pubDate)
            
            if postlist.count()==0:
                continue
                
            item=self.renderBlogPage(
                    'Posts for month %d/%d'%(month,year),
                    start,
                    'blogBriefSite',
                    'monthArchiveSite',
                    None,
                    None,
                    postlist=postlist
                )
            contents+=item
            
        body=contents
        dname=os.path.join(self.dest_dir,'weblog',str(year))
        fname='index.html'
        self.renderBlogPage(
            '%s for year %d'%(self.blog_title,year),
            datetime.datetime(year=year,day=1,month=1),
            None,
            'pageSite',
            dname,
            fname,
            body=body
            )
            
            
                
    def renderBlog(self):
        plist=Post.select(orderBy=Post.q.pubDate)
        oldest=plist[0].pubDate
        newest=plist[-1].pubDate

        self.renderStories()        
        self.renderBlogIndex()
        for year in range(oldest.year,newest.year+1):
            self.renderBlogYear(year)
                
