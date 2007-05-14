# -*- coding: utf-8 -*-

import os,sys
import xmlrpclib
from BartleBlog.backend.dbclasses import *
import sqlobject
import re

def importAdv(username,password):

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
    sp1=re.compile('(href="/)')
    l=sp1.split(text)
    for i in range(0,len(l)):
        if l[i].lower()=='href="/':
            l[i]='href="http://advogato.org/'
    text=''.join(l)

    return text


if __name__ == "__main__":
    initDB('blog.db')
    importAdv(sys.argv[1],sys.argv[2])
