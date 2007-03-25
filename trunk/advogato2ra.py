# -*- coding: utf-8 -*-

import os,sys
import xmlrpclib
from dbclasses import *
import sqlobject
import re

def initDB(name):
    #Initialize sqlobject
    
    db_fname=os.path.abspath(name)
    
    connection_string='sqlite:'+db_fname
    connection=connectionForURI(connection_string)
    sqlhub.processConnection = connection

    if not os.path.exists(db_fname):
        Post.createTable()
        Story.createTable()
        Categories.createTable()
        PostCategories.createTable()
        StoryCategories.createTable()

def importAdv():
    username=sys.argv[1]
    password=sys.argv[2]

    server = xmlrpclib.Server("http://www.advogato.org/XMLRPC",use_datetime=True)
    cookie=server.authenticate(username,password)
    
    length=server.diary.len(username)
    for i in range(0,length):
        print "%d of %d"%(i,length)
        created,updated=server.diary.getDates(username,i)
        
        html=fixLinks(server.diary.get(username,i))
        p=Post(postID="ADV%d"%i,
            title="Advogato post for %s"%str(created),
            link="",
            source="",
            sourceUrl="",
            text=html,
            rendered=html,
            onHome=True,
            structured=False,
            pubDate=created
            )

def fixLinks(text):
         sp1=re.compile("(<person>|</person>)")
         l=sp1.split(text)
         for i in range(0,len(l)):
            if l[i].lower()=='<person>':
                l[i]="<a href='http://advogato.org/person/%s'>"%l[i+1]
            elif l[i].lower()=='</person>':
                l[i]="</a>"
         text=''.join(l)

         sp1=re.compile("(<project>|</project>|<proj>|</proj>)")
         l=sp1.split(text)
         for i in range(0,len(l)):
            if l[i].lower() in ['<project>','<proj>']:
                l[i]="<a href='http://advogato.org/proj/%s'>"%l[i+1]
            elif l[i].lower() in ['</project>','</proj>']:
                l[i]="</a>"
         return ''.join(l)
         
initDB('blog.db')
importAdv()

