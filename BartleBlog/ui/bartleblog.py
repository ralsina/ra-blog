#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys
import os
import datetime

import docutils.core
from cherrytemplate import renderTemplate
from PyQt4 import QtGui, QtCore

import BartleBlog.backend.dbclasses as db
import BartleBlog.backend.macros as macros
from BartleBlog.backend.blog import Blog

from BartleBlog.ui.Ui_mainwindow import Ui_MainWindow
from BartleBlog.ui.config import ConfigWindow
from BartleBlog.ui.editor import EditorWindow

from BartleBlog.ui.postmodel import *
from BartleBlog.rst import rst2html

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Set up the UI from designer
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.blog=Blog()
        self.model=PostModel()

        QtCore.QObject.connect(self.ui.tree,
            QtCore.SIGNAL("activated(QModelIndex)"),
            self.openItem)

        QtCore.QObject.connect(self.ui.actionRender_Blog,
            QtCore.SIGNAL("triggered()"),
            self.renderBlog)

        QtCore.QObject.connect(self.ui.actionConfigure,
            QtCore.SIGNAL("triggered()"),
            self.configure)
            
        QtCore.QObject.connect(self.ui.actionEditPost,
            QtCore.SIGNAL("triggered()"),
            self.edit)

        QtCore.QObject.connect(self.ui.actionNewPost,
            QtCore.SIGNAL("triggered()"),
            self.newPost)
            
        self.curPost=None

        self.ui.viewer.document().setDefaultStyleSheet(open("/home/ralsina/.PyDS/www/static/pyds.css","r").read())
        self.renderTemplate=None

    def edit(self):
        self.editor=EditorWindow(self.curPost)
        QtCore.QObject.connect(self.editor,QtCore.SIGNAL('saved'),self.init_tree)
        self.editor.show()

    def newPost(self):
        self.editor=EditorWindow()
        QtCore.QObject.connect(self.editor,QtCore.SIGNAL('saved'),self.init_tree)
        self.editor.show()
        
    def configure(self):
        cfg=ConfigWindow()
        cfg.exec_()
        
    def renderBlog(self):
        self.blog.renderBlog()

    def init_tree(self):
        self.model=PostModel()
        self.ui.tree.setModel(self.model)

    def openItem(self,index):
        treeitem=index.internalPointer()
        if isinstance(treeitem,PostItem):
            self.renderTemplate='postRender'
            self.curPost=Post.select(Post.q.postID==treeitem.id)[0]
        elif isinstance(treeitem,StoryItem):
            self.renderTemplate='storyRender'
            self.curPost=Story.select(Story.q.postID==treeitem.id)[0]
        else:
            #Maybe clear the views?
            return
        self.displayPostInViewer()

    def displayPostInViewer(self):
            # Fancier HTML for the user
        post=self.curPost
        
        if post.is_dirty:
            self.reRenderCurrentPost()
        
        html=renderTemplate(self.blog.loadTemplate(self.renderTemplate))
        self.ui.viewer.setHtml(html)

    def reRenderCurrentPost(self):
        if self.curPost:
            html=rst2html(self.curPost.text)

            # Basic HTML for the DB
            # FIXME notice RST errors
            self.curPost.rendered=html
            self.curPost.is_dirty=False
            self.displayPostInViewer()

def main():
    app=QtGui.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    window.init_tree()
    sys.exit(app.exec_())

main()
