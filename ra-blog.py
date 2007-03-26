#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys
from PyQt4 import QtGui, QtCore
from Ui_mainwindow import Ui_MainWindow
import os,sys
from dbclasses import Post,Story
from postmodel import *
import datetime
import docutils.core
from cherrytemplate import renderTemplate
import macros

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # Set up the UI from designer
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.blog=Blog()
        self.model=PostModel()
        
        self.ui.actionEdit_Item.setCheckable(True)
        
        QtCore.QObject.connect(self.ui.tree,
            QtCore.SIGNAL("activated(QModelIndex)"),
            self.openItem)
            
        QtCore.QObject.connect(self.ui.actionEdit_Item,
            QtCore.SIGNAL("toggled(bool)"),
            self.switchEditMode)
            
        QtCore.QObject.connect(self.ui.actionRender_Blog,
            QtCore.SIGNAL("triggered()"),
            self.renderBlog)

        self.ui.stack.setCurrentIndex(0)
        self.curPost=None
        
        self.ui.viewer.document().setDefaultStyleSheet(open("/home/ralsina/.PyDS/www/static/pyds.css","r").read())
        self.renderTemplate=None

    def renderBlog(self):
                
        # Render entry page with 20 latest posts
        blog_dir=os.path.join(dest_dir,'weblog')
        if not os.path.exists(blog_dir):
            os.makedirs(blog_dir)
        plist=Post.select(orderBy=Post.q.pubDate)
        postlist=plist[-20:]
        postlist.reverse()
        title=blog_title
        curDate=postlist[0].pubDate
        body=renderTemplate(templates['blogSite'])
        page=renderTemplate(templates['pageSite'])
        fname=os.path.join(blog_dir,"index.html")
        if os.path.exists(fname):
            os.unlink(fname)
        f=codecs.open(fname,"w","utf-8")
        f.write(page)

        # RSS feed with same posts
        page=renderTemplate(templates['feedRSS'])
        fname=os.path.join(blog_dir,"rss.xml")
        if os.path.exists(fname):
            os.unlink(fname)
        f=codecs.open(fname,"w","utf-8")
        f.write(page)
        
        # Render page for each day since beginning
        # of time
        oldest=plist[0].pubDate
        newest=plist[-1].pubDate
        
        current=oldest.replace(hour=0,minute=0,second=0)        
        while current<=newest:
            next=current+datetime.timedelta(1);
            postlist=Post.select(AND(Post.q.pubDate>=current,Post.q.pubDate<next),orderBy=Post.q.pubDate)
            if postlist.count()>0:
                curDate=postlist[0].pubDate
                fname=os.path.join(blog_dir,str(current.year),"%02d"%current.month)
                if not os.path.exists(fname):
                    os.makedirs(fname)
                fname=os.path.join(fname,"%02d.html"%current.day)
                title="%s for %s"%(blog_title,str(current))
                body=renderTemplate(templates['blogSite'])
                page=renderTemplate(templates['pageSite'])
                if os.path.exists(fname):
                    os.unlink(fname)
                f=codecs.open(fname,"w","utf-8")
                f.write(page)
            current=next
        
    def init_tree(self):
        self.ui.tree.setModel(self.model)
        
    def openItem(self,index):
        treeitem=index.internalPointer()
        if self.ui.editor.document().isModified():
            self.reRenderCurrentPost()
        if isinstance(treeitem,PostItem):            
            self.renderTemplate='postRender'
            self.curPost=Post.select(Post.q.postID==treeitem.id)[0]
            self.ui.link.setText(self.curPost.link)
        elif isinstance(treeitem,StoryItem):
            self.renderTemplate='storyRender'
            self.curPost=Story.select(Story.q.postID==treeitem.id)[0]
        else:
            #Maybe clear the views?
            return
        self.ui.categories.setText(','.join([x.nameID for x in self.curPost.categories]))
        self.ui.editor.setText(self.curPost.text)
        self.ui.editor.document().setModified(False)
        self.ui.title.setText(self.curPost.title)
        self.displayPostInViewer()
        self.switchEditMode(self.ui.actionEdit_Item.isChecked())
        
    def displayPostInViewer(self):
            # Fancier HTML for the user
            post=self.curPost
            html=renderTemplate(templates[self.renderTemplate])
            self.ui.viewer.setHtml(html)
        
    def reRenderCurrentPost(self):
        if self.curPost:
            self.curPost.text=str(self.ui.editor.document().toPlainText())
            html=docutils.core.publish_parts(self.curPost.text,writer_name='html')['fragment']
            
            # Basic HTML for the DB
            self.curPost.rendered=html
            self.displayPostInViewer()
            
                    
    def switchEditMode(self,mode):
        if mode==1:
            self.ui.stack.setCurrentIndex(1)
            self.ui.editor.setFocus()
        else:
            self.ui.stack.setCurrentIndex(0)
            if self.ui.editor.document().isModified():
                self.reRenderCurrentPost()
            self.ui.viewer.setFocus()
        
def main():
    app=QtGui.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    window.init_tree()
    sys.exit(app.exec_())
    
main()
