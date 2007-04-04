# -*- coding: utf-8 -*-

import os,sys,datetime,codecs

from cherrytemplate import renderTemplate

import dbclasses as db
from macros import Macros

from BartleBlog.util import slimmer

class Blog:

    def __init__(self):
        db.initDB('blog.db')
        self.dest_dir=os.path.abspath("weblog")
        self.blog_title="Lateral Opinion"

        #################################################################################
        ### Things that should be in the config file
        #################################################################################

        self.blogName="Lateral Opinion"
        self.basepath=u"http://lateral.blogsite.org/"
        self.author=u"Roberto Alsina"
        self.author_email=u"ralsina@kde.org"
        self.description=u"Roberto Alsina's blog"
        self.language="en"
        self.version="Bartleblog 0.0"

        Macros(self)

    def loadTemplate(self,name):
        fname=os.path.abspath('templates/%s.tmpl'%name)
        f=codecs.open(fname,"r","utf-8")
        return f.read()

    def renderBlogPage(self,title,curDate,itemtmpl,pagetmpl,dname,fname,postlist=None,story=None,body=None,bodytitle=None):
        macros=self.macros
        blog=self
        # Render
        if body or body=="":
            pass
        else:
            body=renderTemplate(self.loadTemplate(itemtmpl))

        if pagetmpl:
            page=renderTemplate(self.loadTemplate(pagetmpl))
        else:
            page=body
        #page=slimmer.html_slimmer(page)
        # Save or return
        if not fname:
            return page
        if not os.path.exists(dname):
            os.makedirs(dname)
        if os.path.exists(fname):
            os.unlink(fname)
        f=codecs.open(os.path.join(dname,fname),"w","utf-8")
        f.write(page)

    def renderRSS(self,title,curDate,dname,fname,postlist):
        macros=self.macros
        blog=self
        rss=renderTemplate(self.loadTemplate('feedRSS'))
        if not os.path.exists(dname):
            os.makedirs(dname)
        if os.path.exists(fname):
            os.unlink(fname)
        f=codecs.open(os.path.join(dname,fname),"w","utf-8")
        f.write(rss)

    def renderCategory(self,cat):
        catname=cat.name.lower()
        title='Posts in %s about %s'%(self.blog_title,cat.name)
        dname=os.path.join(self.dest_dir,'categories')
        fname=catname+'.html'
        postlist=cat.posts
        curDate=datetime.datetime.today()
        self.renderBlogPage(
                title,
                curDate,
                'blogBriefSite',
                'pageSite',
                dname,
                fname,
                postlist=postlist,
                bodytitle=title
            )
        self.renderRSS(title,curDate,dname,catname+'.xml',postlist)

    def renderCategoryIndex(self):
        title='%s posts by topic'%self.blog_title
        dname=os.path.join(self.dest_dir,'categories')
        fname='index.html'
        curDate=datetime.datetime.today()
        self.renderBlogPage(
                title,
                curDate,
                'categorySite',
                'pageSite',
                dname,
                fname,
                postlist=db.Category.select()
            )

    def renderCategories(self):
        self.renderCategoryIndex()
        for cat in db.Category.select():
            self.renderCategory(cat)

    def renderStoryIndex(self):
        dname=os.path.join(self.dest_dir,'stories')
        fname="index.html"
        postlist=db.Story.select(orderBy=db.Story.q.pubDate)
        title="%s - Story Index"%self.blog_title
        curDate=datetime.datetime.today()
        self.renderBlogPage(
                title,
                curDate,
                'storyIndex',
                'pageSite',
                dname,
                fname,
                postlist=postlist,
                bodytitle='%s posts by topic'%self.blogName
            )
        self.renderRSS(title,curDate,dname,'rss.xml',postlist)

    def renderStories(self):

        self.renderStoryIndex()

        # Render stories
        story_dir=os.path.join(self.dest_dir,'stories')
        for story in db.Story.select():
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
        postlist=list(db.Post.select(orderBy=db.Post.q.pubDate).reversed()[:20])
        curDate=postlist[0].pubDate
        title=self.blog_title
        dname=os.path.join(self.dest_dir,"weblog")
        self.renderRSS(title,curDate,dname,'rss.xml',postlist)
        self.renderBlogPage(
                title,
                curDate,
                'blogSite',
                'pageSite',
                dname,
                'index.html',
                postlist=postlist
            )

    def renderBlogDay(self,date):
        start=date.replace(hour=0,minute=0,second=0)
        end=date+datetime.timedelta(1)
        postlist=db.Post.select(db.AND(db.Post.q.pubDate>=start,db.Post.q.pubDate<end))
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

        postlist=db.Post.select(db.AND(db.Post.q.pubDate>=start,db.Post.q.pubDate<end),
                                orderBy=db.Post.q.pubDate)
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

            postlist=db.Post.select(db.AND(db.Post.q.pubDate>=start,db.Post.q.pubDate<end),
                                orderBy=db.Post.q.pubDate)

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

    def renderBlogArchive(self,start,end):
        body='<div class="yui-u rounded postbox thinedge"><h1>%s</h1><ul>%s</ul></div>'%(self.blog_title,''.join( [ '<li><a href="%s">%d</a>'%(self.macros.absoluteUrl('weblog/%d/index.html'%y),y) for y in range(start,end+1) ]))

        dname=os.path.join(self.dest_dir,'weblog')
        fname='archive.html'

        self.renderBlogPage(
            '%s Archives'%(self.blog_title),
            datetime.datetime.today(),
            None,
            'pageSite',
            dname,
            fname,
            body=body
            )


    def renderBlog(self):
        plist=db.Post.select(orderBy=db.Post.q.pubDate)
        oldest=plist[0].pubDate
        newest=plist[-1].pubDate

        self.renderCategories()
        self.renderBlogArchive(oldest.year,newest.year)
        self.renderStories()
        self.renderBlogIndex()
        for year in range(oldest.year,newest.year+1):
            self.renderBlogYear(year)
