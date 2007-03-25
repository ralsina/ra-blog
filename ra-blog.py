#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys
from PyQt4 import QtGui, QtCore
from Ui_mainwindow import Ui_MainWindow
from sqlobject import *
import os,sys
from dbclasses import *
from postmodel import *
import datetime
import docutils.core
from cherrytemplate import renderTemplate
import macros

dest_dir=os.path.abspath("weblog")
blog_title="Lateral Opinion"

templates={
    'postRender':u'''
    <h1>
    <py-if="post.link">
        <a href='<py-eval="post.link">'><py-eval="post.title"></a>
    </py-if>
    <py-else>
        <py-eval="post.title">
    </py-else>
    </h1>
    <py-eval="post.rendered">
    ''',
    'storyRender':'''
    <h1>
    <py-eval="post.title">
    </h1>
    <py-eval="post.rendered">
    ''',
    'storySite':u'''    
<div class="storybox">
  <h1><py-eval="story.title"></h1>
  <table width="100%">
  <tr>
    <td align=center>
      <a href=http://feeds.feedburner.com/LateralOpinion">
        <img src="http://feeds.feedburner.com/LateralOpinion.gif" alt="Lateral Opinion" style="border:0">
      </a>
    </td>
  </tr>
  </table>
  
  <py-eval="story.rendered">
  
  <div class="smallbox">
    <py-eval="story.HaloScanComments()">&nbsp;&bull;&nbsp;
    <py-eval="story.HaloScanTB()">
    <br>
    <script src="http://feeds.feedburner.com/~s/LateralOpinionArticles?i=<py-eval="story.myurl()">
    type="text/javascript" charset="utf-8"></script>
    <br>
    last changed <py-eval="str(story.pubDate)">
  </div>
</div>

''',
    'pageSite':u'''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <title><py-eval="title"></title>
    <link rel="stylesheet" href="<py-eval="macros.absoluteUrl('/static/pyds.css')">" type="text/css">
    <link rel="alternate" type="application/rss+xml" title="RSS" href="http://feeds.feedburner.com/LateralOpinion">
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
    <script type="text/javascript" src="http://www.haloscan.com/load/ralsina"> </script>    
</head>
<body>

  <div align="center" >
    <div class="banner" style="margin-top:2em; margin-bottom:1em;">
      <img src="http://cablemodem.fibertel.com.ar/lateral/banner.png" ALT="Lateral Opinion">
    </div>

    <div class="sidebar">    
      <div align="left" class="googlebox">  
          <ul>
            <li>
              <a href="http://lateral.blogsite.org">Home</a>
            </li>
            <li>
              <a href="http://lateral.blogsite.org/stories/">Articles</a>
            </li>      
            <li>
              <a href="http://lateral.blogsite.org/archive/">Archives</a>
            </li>
            <hr>
            <li> Software
              <ul>
                <li>
                  <a href="http://rascan.blogsite.org">RaSCAN</a>
                </li>
                <li>
                  <a href="http://raplugins.blogsite.org">Ra-Plugins</a>
                </li>
                <li>
                  <a href="http://raspf.blogsite.org">RaSPF</a>
                </li>
                <li>
                  <a href="http://cherrytv.blogsite.org">CherryTV</a>
                </li>
              </ul>
            </li>
          </ul>
      </div>
  
      <div align="left" class="googlebox">
        <script type="text/javascript" src="http://embed.technorati.com/embed/tpgux8rtif.js"></script>
      </div>
    
      <div class="whiteboxsmall">
        <py-eval="macros.chunk['first']">
        <py-eval="macros.chunk['second']">
      </div>
    </div>
    </div>
  </div>
  <div class="content">
    <py-eval="body">
    <p>
    <div class="copybox" style="margin:1em;">
      <py-eval="macros.copyright(story.pubDate.year)">
    </div>
  </div>
$macros.webbug()
    
</body>
</html>
    
''',
    'blogSite':u"""
<py-for="post in postlist">
  <div class="postbox">
    <a href="<py-eval="macros.getUrlForDay(post.pubDate)">">
    <py-eval="str(post.pubDate)"></a>
      <py-if="post.link">
        <h2><a name="<py-eval="post.postID">"></a>
            <a href="<py-eval="post.link">"><py-eval="post.title"></a></h2>
      </py-if>
      <py-else>
        <h2><a name="<py-eval="post.postID">"></a>
            <py-eval="post.title"></h2>
      </py-else>
      <py-eval="post.rendered">
    <div class="smallbox">
      <a href="<py-eval="macros.weblogPermaLink(post)">">#</a>&nbsp;&bull;&nbsp;
      <py-eval="post.HaloScanComments()">&nbsp;&bull;&nbsp;
      <py-eval="post.HaloScanTB()">&nbsp;&bull;&nbsp;
      <py-eval="post.Talkr()">
      <py-if="post.link">
        &nbsp;&bull;&nbsp;<a class=reference href="<py-eval="post.link">">Read More</a>
      </py-if>
      <br>
      <py-eval="post.FeedBurnerFlare()">
      <py-eval="post.TechnoratiTags()">
    </div>
  </div>
</py-for>
"""

}


        
    

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # Set up the UI from designer
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        db_fname=os.path.abspath('blog.db')
        connection_string='sqlite:'+db_fname
        connection=connectionForURI(connection_string)
        sqlhub.processConnection = connection
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
    
        # Render stories
        story_dir=os.path.join(dest_dir,'stories')        
        if not os.path.exists(story_dir):
            os.makedirs(story_dir)
        for story in Story.select():
            title=story.title
            body=renderTemplate(templates['storySite'],inputEncoding='utf8')
            page=renderTemplate(templates['pageSite'])
            fname="%s/%s.html"%(story_dir,story.postID)
            if os.path.exists(fname):
                os.unlink(fname)
            f=codecs.open(fname,"w","utf-8")
            f.write(page)
            
        # Render entry page with 20 latest posts
        blog_dir=os.path.join(dest_dir,'weblog')
        if not os.path.exists(blog_dir):
            os.makedirs(blog_dir)
        plist=Post.select(orderBy=Post.q.pubDate)
        postlist=plist[-20:]
        postlist.reverse()
        title=blog_title
        body=renderTemplate(templates['blogSite'])
        page=renderTemplate(templates['pageSite'])
        fname=os.path.join(blog_dir,"index.html")
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
