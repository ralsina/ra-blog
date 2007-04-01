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
from BartleBLog.ui.config import ConfigWindow

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

        QtCore.QObject.connect(self.ui.actionConfigure,
            QtCore.SIGNAL("triggered()"),
            self.configure)
            
            
        self.ui.stack.setCurrentIndex(0)
        self.curPost=None

        self.ui.viewer.document().setDefaultStyleSheet(open("/home/ralsina/.PyDS/www/static/pyds.css","r").read())
        self.renderTemplate=None

    def configure(self):
        cfg=ConfigWindow()
        cfg.exec_()
        
    def renderBlog(self):
        self.blog.renderBlog()

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
        self.ui.categories.setText(','.join([x.name for x in self.curPost.categories]))
        self.ui.editor.setText(self.curPost.text)
        self.ui.editor.document().setModified(False)
        self.ui.title.setText(self.curPost.title)
        self.displayPostInViewer()
        self.switchEditMode(self.ui.actionEdit_Item.isChecked())

    def displayPostInViewer(self):
            # Fancier HTML for the user
        post=self.curPost
        html=renderTemplate(self.blog.loadTemplate(self.renderTemplate))
        self.ui.viewer.setHtml(html)

    def reRenderCurrentPost(self):
        if self.curPost:
            self.curPost.text=str(self.ui.editor.document().toPlainText())
            html=rst2html(self.curPost.text)

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
