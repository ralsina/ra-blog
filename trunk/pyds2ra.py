#!/usr/bin/env python
# -*- coding: utf-8 -*-


import metakit,os,datetime,time
from dbclasses import *
import sys        

def initDB(name):
    #Initialize sqlobject
    
    db_fname=os.path.abspath(name)
    if os.path.exists(db_fname):
        os.unlink(db_fname)
    
    connection_string='sqlite:'+db_fname
    connection=connectionForURI(connection_string)
    sqlhub.processConnection = connection

    Post.createTable()
    Story.createTable()
    Categories.createTable()
    PostCategories.createTable()
    StoryCategories.createTable()

def importWeblog():

    # Initialize metakit
    
    mdb=metakit.storage(os.path.expanduser("~/.PyDS/var/weblog.data"),0)
    v=mdb.getas("posts[id:S,title:S,link:S,source:S,sourceurl:S,text:\
    S,rendered:S,localrendered:S,onhome:I,structured:I,pubdate:S\
    ,pubtime:F,categories[name:S]]")
    
    for p in v:
        post=Post(postID=p.id,
            title=unicode(p.title.decode('latin-1')),
            link=unicode(p.link.decode('latin-1')),
            source=unicode(p.source.decode('latin-1')),
            sourceUrl=p.sourceurl,
            text=unicode(p.text.decode('latin-1')),
            rendered=unicode(p.rendered.decode('latin-1')),
            onHome=p.onhome,
            structured=p.structured,
            pubDate=datetime.datetime.fromtimestamp(p.pubtime)
            )
        for cat in p.categories:            
            c=PostCategories(postID=post.id,name=cat.name)
            
def importStories():
    # Initialize metakit
    
    mdb=metakit.storage(os.path.expanduser("~/.PyDS/var/stories.data"),0)
    v=mdb.getas('stories[id:I,pubtime:F,title:S,desc:S,\
        text:S,rendered:S,structured:I,draft:I,\
        renderhook:S,quiet:I]')
    
    for p in v:
        story=Story(postID=str(p.id),
            title=unicode(p.title.decode('latin-1')),
            desc=unicode(p.desc.decode('latin-1')),
            text=unicode(p.text.decode('latin-1')),
            rendered=unicode(p.rendered.decode('latin-1')),
            structured=p.structured,
            draft=p.draft,
            quiet=p.quiet,
            pubDate=datetime.datetime.fromtimestamp(p.pubtime)
            )

initDB('blog.db')
importStories()
importWeblog()

