# -*- coding: utf-8 -*-

import os,sys,datetime,codecs,re

from mako.template import Template
from mako.lookup import TemplateLookup

import dbclasses as db
from macros import Macros
import shutil

from BartleBlog.util import slimmer,PyRSS2Gen
import BartleBlog.backend.config as config

import datetime


class Blog:
    def __init__(self):

        dn=os.path.expanduser('~/.bartleblog')
        db.initDB(os.path.join(dn,'blog.db'))

        self.loadConfig()
        
        self.progress=None

        self.dayHooks=[]
        self.monthHooks=[]
        self.yearHooks=[]
        self.lookup = TemplateLookup(directories=[os.path.expanduser('~/.bartleblog/templates'), '.'], 
                                                                     module_directory=os.path.expanduser('~/.bartleblog/mako_modules'))
        
        Macros(self)
        if config.firstRun:
            self.setupTree()

    def setupTree(self):
        '''Setup things in ~/.bartleblog: templates/static/js/calendar/etc.'''
        print 'Setting up tree'
        #FIXME: this path should be from a standard location
        if not os.path.isdir(os.path.expanduser('~/.bartleblog/weblog')):
            os.makedirs(os.path.expanduser('~/.bartleblog/weblog'))
        if not os.path.isdir(os.path.expanduser('~/.bartleblog/templates')):
            shutil.copytree(os.path.abspath('templates'),os.path.expanduser('~/.bartleblog/templates'))
        if not os.path.isdir(os.path.expanduser('~/.bartleblog/weblog/static')):
            shutil.copytree(os.path.abspath('static'),os.path.expanduser('~/.bartleblog/weblog/static'))
        if not os.path.isdir(os.path.expanduser('~/.bartleblog/resources')):
            shutil.copytree(os.path.abspath('resources'),os.path.expanduser('~/.bartleblog/resources'))
        
    def loadConfig(self):
        self.blog_title=config.getValue('blog', 'title', 'My First Blog')
        self.blog_subtitle=config.getValue('blog', 'subtitle', 'A Blog')
        self.basepath=config.getValue('blog', 'url', 'http://some.host/some_path/')
        if self.basepath[-1]<>'/':
            self.basepath+='/'
        self.url=self.basepath
        self.author=config.getValue('blog', 'author', 'Joe Doe') 
        self.author_email=config.getValue('blog', 'email', 'joe@doe')
        self.description=config.getValue('blog', 'description', 'My Blog')
        self.dest_dir=config.getValue('blog', 'folder', os.path.expanduser("~/.bartleblog/weblog"))
        if not os.path.isdir(self.dest_dir):
            os.mkdir(self.dest_dir)
        
        self.version="Bartleblog 0.0"

    def loadTemplate(self,name):
        fname=os.path.abspath('templates/%s.tmpl'%name)
        f=codecs.open(fname,"r","utf-8")
        return f.read()

    def renderRSS(self,title,curDate,dname,fname,postlist,lang=None):
#        template = self.lookup.get_template('feedRSS.tmpl')
#        if not lang:
#            langcode=config.getValue('blog', 'langcode', 'en')
#        else:
#            langcode=lang.code
#
#        rss=template.render_unicode(title=title, curDate=curDate, 
#                                    postlist=postlist, macros=self.macros, 
#                                    blog=self, langcode=langcode, lang=lang)
#        if not os.path.exists(dname):
#            os.makedirs(dname)
#        if os.path.exists(fname):
#            os.unlink(fname)

        items=[]
        for post in postlist:
          tpost = post.translated(lang)
          args= {
                'title' : tpost.title, 
                'link'  : getattr(tpost, 'link', None), 
                'description' : tpost.rendered, 
                'guid' : self.macros.absoluteUrl(post.myurl(lang)), 
                'pubDate' : post.pubDate

          }
          if not args['link']: del (args['link']) 
          items.append(
              PyRSS2Gen.RSSItem(**args)
            )

          rss = PyRSS2Gen.RSS2(
                title = title, 
                link  = self.basepath, 
                description = self.description, 
                lastBuildDate = curDate, 
                items = items
          )

#        f=codecs.open(os.path.join(dname,fname),"w","utf-8")
          f=open(os.path.join(dname,fname),"w")
          rss.write_xml(f)
          
    def renderMakoPage(self, template, dname, fname, **kwargs):
        kwargs['macros']=self.macros
        kwargs['blog']=self
        if not 'lang' in kwargs:
            kwargs['lang']=None
        if kwargs['lang'] and kwargs['lang']<>'en': # translated template
          template_tr=template+"."+kwargs['lang'].code
          try:
            print "Got ", template_tr
            template = self.lookup.get_template(template_tr)
          except: # Maybe the translated template doesn't exist
            print "Got ", template
            template = self.lookup.get_template(template)
        else:
          print "Got ", template
          template = self.lookup.get_template(template)
          
        page=template.render_unicode(**kwargs)
        if not os.path.exists(dname):
            os.makedirs(dname)
        if os.path.exists(fname):
            os.unlink(fname)
        f=codecs.open(os.path.join(dname,fname),"w","utf-8")
        f.write(page)
        print 'saving: ', os.path.join(dname,fname)
        

    def renderCategoryIndex(self):
        title='%s posts by topic'%self.blog_title
        dname=os.path.join(self.dest_dir,'categories')
        fname='index.html'
        curDate=datetime.datetime.today()
        self.renderMakoPage(
                'categoryIndexSite.tmpl', 
                dname,
                fname,
                catlist=db.Category.select(),
                title=title,
                curDate=curDate
            )

    def renderCategory(self,cat):
        if not cat:
            return
        catname=cat.name.lower()
        title='Posts in %s about %s'%(self.blog_title,cat.name)
        dname=os.path.join(self.dest_dir,'categories')
        fname=catname+'.html'
        postlist=cat.posts
        postlist.reverse()
        stlist=cat.stories
        stlist.reverse()
        curDate=datetime.datetime.today()
        self.renderRSS(title,curDate,dname,catname+'.xml',postlist[:50])
        self.renderMakoPage(
                'categorySite.tmpl',
                dname,
                fname,
                title=title,
                curDate=curDate,
                postlist=postlist,
                storylist=stlist, 
                cat=cat
            )
        # Now the translations
        for tr in db.Translation.select():
            self.renderRSS(title,curDate,dname,catname+'-'+tr.code+'.xml',postlist[:50],lang=tr)
        
    def renderBlogMonth(self,date):
        start=date.replace(day=1,hour=0,minute=0,second=0)
        end=start
        if start.month==12:
            end=end.replace(year=start.year+1,day=1,month=1)
        else:
            end=end.replace(month=start.month+1)

        postlist=db.Post.select(db.AND(db.Post.q.pubDate>=start,db.Post.q.pubDate<end),
                                orderBy='-pubDate')
        if postlist.count()==0:
            return

        # Variables used by the templates
        title="%s for %d/%d"%(self.blog_title, start.month, start.year)
        curDate=postlist[0].pubDate
        dname=os.path.join(self.dest_dir,"weblog/%d/%02d"%(date.year,date.month))
        fname="index.html"

        self.renderMakoPage(
                'blogSite.tmpl',
                dname,
                fname, 
                title=title,
                curDate=curDate, 
                postlist=postlist 
            )

        # FIXME: this should not be necessary, check it out
            
#        for day in range(1,32):
#            try:
#                self.renderBlogDay(curDate.replace(day=day))
#            except ValueError:
#                #To avoid checking month length
#                pass
                
        # Render tool hooks for months        
        for hook in self.monthHooks:
            apply(hook,[date])

    def renderCategories(self):
        self.renderCategoryIndex()
        for cat in db.Category.select():
            self.renderCategory(cat)

    def renderStoryIndex(self):
        dname=os.path.join(self.dest_dir,'stories')
        fname="index.html"
        storylist=db.Story.select(orderBy='-pubDate')
        title="%s - Story Index"%self.blog_title
        curDate=datetime.datetime.today()
        self.renderMakoPage(
                'storyIndexSite.tmpl',
                dname,
                fname,
                title=title,
                curDate=curDate,
                storylist=storylist,
            )
        self.renderRSS(title,curDate,dname,'rss.xml',storylist)

    def renderStory(self,story):
        story_dir=os.path.join(self.dest_dir,'stories')
        title=story.title
        curDate=story.pubDate
        fname="%s.html"%(story.postID)
        self.renderMakoPage(                
                'storySite.tmpl',
                story_dir,
                fname,
                title=title,
                curDate=curDate,
                story=story
                )
        # Now the translations
        for tr in db.Translation.select():
            lang=tr
            dname=os.path.join(self.dest_dir,"tr",lang.code,"stories")
            self.renderMakoPage(
                    'storySite.tmpl', 
                    dname,
                    fname,
                    title=title,
                    curDate=curDate,
                    story=story,
                    lang=lang
                )
        
    def renderStories(self):
        self.renderStoryIndex()
        for story in db.Story.select():
            self.renderStory(story)
            if self.progress: self.progress.step()

    def renderBlogIndexPage(self,pageNumber):
        postlist=db.Post.select(orderBy='-pubDate')
        c=postlist.count()
        if c<=pageNumber*10: # It would be an empty page
          return
        if c:
            curDate=postlist[0].pubDate
        else:
            curDate=datetime.datetime.today()
        # First the default lang
        title=self.blog_title
        dname=os.path.join(self.dest_dir,"weblog")
        numPages=int(postlist.count()/10)
        if pageNumber==0: #FIXME Extra page, this should be cleaner
          self.renderRSS(title,curDate,dname,'rss.xml',postlist[0:20])
          self.renderMakoPage(
                  'blogSite.tmpl', 
                  dname,
                  'index.html',
                  title=title,
                  curDate=curDate,
                  postlist=postlist[:10],
                  curPage=0,
                  numPages=numPages,
                  pagTempl="/weblog/index-%d.html"
              )
        self.renderMakoPage(
                'blogSite.tmpl', 
                dname,
                'index-%d.html'%(pageNumber),
                title=title,
                curDate=curDate,
                postlist=postlist[pageNumber*10:pageNumber*10+10],
                curPage=pageNumber,
                numPages=numPages,
                pagTempl="/weblog/index-%d.html"
            )
        # Now the translations
        for tr in db.Translation.select():
            lang=tr
            dname=os.path.join(self.dest_dir,"tr",lang.code,"weblog")
            if pageNumber==0: #FIXME Extra page, this should be cleaner
              self.renderRSS(title,curDate,dname,'rss.xml',postlist[0:20],lang=lang)
              self.renderMakoPage(
                      'blogSite.tmpl', 
                      dname,
                      'index.html',
                      title=title,
                      curDate=curDate,
                      postlist=postlist[:10],
                      lang=lang,
                      curPage=0,
                      numPages=numPages,
                      pagTempl="/weblog/tr/%s/index-%%d.html"%lang.code
                  )
            self.renderMakoPage(
                    'blogSite.tmpl', 
                    dname,
                    'index-%d.html'%(pageNumber),
                    title=title,
                    curDate=curDate,
                    postlist=postlist[pageNumber*10:pageNumber*10+10], 
                    lang=lang,
                    curPage=pageNumber,
                    numPages=numPages,
                    pagTempl="/weblog/tr/%s/index-%%d.html"%lang.code
                )

    def renderBlogIndex(self):
        
        title=self.blog_title
        dname=os.path.join(self.dest_dir,"weblog")
        postlist=db.Post.select(orderBy='-pubDate')
        c=postlist.count()
        if c:
            curDate=postlist[0].pubDate
        else:
            curDate=datetime.datetime.today()
        numPages=int(postlist.count()/10)
        
        self.renderRSS(title,curDate,dname,'rss.xml',postlist[0:20])
        for i in range(0,numPages+1):
          self.renderBlogIndexPage(i)
        # Now the translations
        for tr in db.Translation.select():
            lang=tr
            dname=os.path.join(self.dest_dir,"tr",lang.code,"weblog")
            self.renderRSS(title,curDate,dname,'rss.xml',postlist[0:20],lang=lang)
            for i in range(0,numPages+1):
              self.renderBlogIndexPage(i)
            

    def renderBlogDay(self,date):
        start=date.replace(hour=0,minute=0,second=0)
        end=date+datetime.timedelta(1)
        postlist=db.Post.select(db.AND(db.Post.q.pubDate>=start,db.Post.q.pubDate<end), orderBy='-pubDate')
        if postlist.count()==0:
            return

        # Variables used by the templates
        title="%s for %d/%d/%d"%(self.blog_title, start.day, start.month, start.year)
        curDate=postlist[0].pubDate
        dname=os.path.join(self.dest_dir,"weblog/%d/%02d"%(date.year,date.month))
        fname="%02d.html"%(date.day)

        self.renderMakoPage(
                'blogSite.tmpl', 
                dname,
                fname,
                title=title,
                curDate=curDate,
                postlist=postlist
            )

        # Now the translations
        for tr in db.Translation.select():
            lang=tr
            dname=os.path.join(self.dest_dir,"tr",lang.code,"weblog/%d/%02d"%(date.year,date.month))
            self.renderMakoPage(
                    'blogSite.tmpl', 
                    dname,
                    fname,
                    title=title,
                    curDate=curDate,
                    postlist=postlist, 
                    lang=lang
                )
        # Render tool hooks for days
        for hook in self.dayHooks:
            apply(hook,[date])

    def renderBlogPostPreview(self, postID):
        post=db.postPreviewById(postID)
        if not post: # Previews get deleted often
            return
        print postID, post        
        self.renderMakoPage('blogSite.tmpl',
                            os.path.join(self.dest_dir,"preview"), 
                            postID, 
                            title=self.blog_title+' - preview', 
                            curDate=datetime.datetime.today(), 
                            postlist=[post]
                            )



    def renderOnePost(self,postfile):
        postID=postfile[:-5]
        post=db.postById(postID)
        self.renderMakoPage('onePostSite.tmpl',
                            os.path.join(self.dest_dir,"weblog","posts"),
                            postfile,
                            title=post.title,
                            curDate=post.pubDate,
                            postlist=[post]
                            )

        # Now the translations
        for tr in db.Translation.select():
            lang=tr
            tpost=post.translated(lang)
            dname=os.path.join(self.dest_dir,"tr",lang.code,"weblog","posts")
            self.renderMakoPage('onePostSite.tmpl',
                                dname,
                                postfile,
                                title=tpost.title,
                                curDate=post.pubDate,
                                postlist=[post],
                                lang=lang
                                )
        # Render tool hooks for days
        for hook in self.dayHooks:
            apply(hook,[date])


    def renderBlogYear(self,year):
        # Yearly archive page
        start=datetime.datetime(year=year,day=1,month=1)
        postlist=[]
        for month in range(1, 13):
            end=start
            if start.month==12:
                end=end.replace(year=start.year+1,day=1,month=1)
            else:
                end=end.replace(month=start.month+1)
            postlist.append(db.Post.select(db.AND(db.Post.q.pubDate>=start,db.Post.q.pubDate<end),
                                           orderBy='pubDate'))
            start=end
            
        self.renderMakoPage ('yearSite.tmpl', 
                             os.path.join(self.dest_dir,'weblog', str(year)), 
                             'index.html', 
                             title='%s for year %d'%(self.blog_title, year),
                             curDate= datetime.datetime(year=year,day=1,month=1), 
                             postlist=postlist, 
                             year=year,
                             macros=self.macros
                             )
        # Render tool hooks for years
        for hook in self.yearHooks:
            apply(hook,[date])

    def renderPage(self, page, lang=None):
        try:
            print "rendering: ",page.path
            path=page.path.split('/')
            if path[0]=='categories':
                if path[1]=='index.html':
                    self.renderCategoryIndex()
                elif len(path)==2:
                    self.renderCategory(db.categoryByName(path[1].split('.')[0]))
                else:
                    raise 'BogusPage'
                    
            elif path[0]=='stories':
                if len(path)==1 or path[1]=='index.html':
                    self.renderStoryIndex()                
                elif len(path)==2:
                    s=db.storyById(path[1].split('.')[0])
                    if s:
                        self.renderStory(s)
                else:
                    raise 'BogusPage'
            elif path[0]=='weblog':
                if len(path)==1:
                    return
                elif path[1]=='index.html':
                    self.renderBlogIndexPage(0)
                elif path[1].startswith("index-"):
                    pnum=re.split('([0-9]*)',path[1])[1]
                    self.renderBlogIndexPage(int(pnum))
                elif len(path)==3:
                    if path[2]=='index.html' and path[1].isdigit():
                        year=int(path[1])
                        self.renderBlogYear(year)
                    elif path[1]=='posts':
                        self.renderOnePost(path[2])
                elif len(path)==4 and path[1].isdigit() and path[2].isdigit():
                    year=int(path[1])
                    month=int(path[2])
                    if path[3]=='index.html':
                        self.renderBlogMonth(datetime.datetime(year=year,month=month,day=1))
                    else:
                        day=int(path[3].split('.')[0])
                        self.renderBlogDay(datetime.datetime(year=year,month=month,day=day))            
                else:
                    pass
                    #raise 'BogusPage'
            elif path[0]=='preview':
                self.renderBlogPostPreview(path[1])
            else:
                pass
                #raise 'BogusPage'
            page.is_dirty=False
        except 'BogusPage':
            print 'Bogus Page: ',page.path
            page.destroySelf()
#        except:
#            #TODO: nicer    
#            print 'Error rendering ', page.path, 'please debug'

                
            
    def renderBlog(self):
        '''Redo all pages marked as dirty'''
        plist=db.Page.select(db.Page.q.is_dirty==True)
        if self.progress:
            self.progress.setSteps(plist.count())
        for p in plist:
            self.renderPage(p)
            if self.progress: self.progress.step()
        if self.progress:
            self.progress.close()

    def renderFullBlog(self):
        if self.progress:
            self.progress.setStages([
            ['Rendering Categories','Rendering index pages for each category.'],
            ['Rendering Stories','Rendering the static story pages'],
            ['Rendering Index','Rendering the main page.'],
            ['Rendering Blog','Rendering all archived posts.']])
        plist=db.Post.select(orderBy='pubDate')
        oldest=plist[0].pubDate
        newest=plist[-1].pubDate

        print "Rendering posts"
        for p in plist:
            self.renderOnePost(p.postID+'.html')
            
        if self.progress:
            self.progress.gotoStage(0)


            c=0
            for cat in db.Category.select():
                c=c+len(cat.posts)+len(cat.stories)
            self.progress.setSteps(c)
        self.renderCategories()

        if self.progress:
            self.progress.gotoStage(1)
            self.progress.setSteps(db.Story.select().count())
        self.renderStories()

        if self.progress: self.progress.gotoStage(2)
        self.renderBlogIndex()

        if self.progress:
            self.progress.gotoStage(3)
            # Each post is rendered once in year/month/day pages
            self.progress.setSteps(plist.count()*3)
            self.progress.setPos(0)
        for year in range(oldest.year,newest.year+1):
            self.renderBlogYear(year)
            for month in range(1,13):
                self.renderBlogMonth(datetime.datetime(year=year,month=month,day=1))
                for day in range(1,32):
                    try:
                        self.renderBlogDay(datetime.datetime(year=year,month=month,day=day))
                    except ValueError:
                        pass
        
                    
        if self.progress:
            self.progress.close()

    def regenerate(self,all=False):
        if self.progress:
            self.progress.setStages([
            ['Regenerating Stories','Converting to HTML your stories.'],
            ['Regenerating Posts','Converting to HTML your posts.']])
        if all:
            plist=db.Post.select()
            slist=db.Story.select()
        else:
            plist=db.Post.select(db.Post.q.is_dirty>1)
            slist=db.Story.select(db.Story.q.is_dirty>1)

        if self.progress:
            self.progress.gotoStage(0)
            self.progress.setSteps(slist.count())
        for s in slist:
            s.render()
            if self.progress:
                self.progress.step()

        if self.progress:
            self.progress.gotoStage(1)
            self.progress.setSteps(plist.count())
        for p in plist:
            p.render()
            if self.progress:
                self.progress.step()

        if self.progress:
            self.progress.close()

        
