#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys
import os
import traceback
import datetime

import docutils.core
from mako.template import Template
from PyQt4 import QtGui, QtCore

import BartleBlog.backend.dbclasses as db
from BartleBlog.backend.blog import Blog

from BartleBlog.ui.Ui_mainwindow import Ui_MainWindow
import BartleBlog.ui.Ui_about
from BartleBlog.ui.config import ConfigWindow
from BartleBlog.ui.editor import EditorWindow
from BartleBlog.ui.storyeditor import StoryEditorWindow
from BartleBlog.ui.progress import ProgressDialog
from BartleBlog.ui.help import HelpWindow
import BartleBlog.backend.config as config
import BartleBlog.backend.preview as preview

from BartleBlog.ui.postmodel import *

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Set up the UI from designer
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        if config.firstRun:
            self.firstRun=True
        else:
            self.firstRun=False

        self.blog=Blog()
        self.model=PostModel()

        if self.firstRun:
            self.blog.setupTree()
            self.configure('blog')

        QtCore.QObject.connect(self.ui.actionAbout_BartleBlog,
            QtCore.SIGNAL("triggered()"),
            self.about)

        QtCore.QObject.connect(self.ui.tree,
            QtCore.SIGNAL("activated(QModelIndex)"),
            self.openItem)

        QtCore.QObject.connect(self.ui.actionRender_Blog,
            QtCore.SIGNAL("triggered()"),
            self.renderBlog)

        QtCore.QObject.connect(self.ui.actionRender_Full_Blog,
            QtCore.SIGNAL("triggered()"),
            self.renderFullBlog)

        QtCore.QObject.connect(self.ui.actionConfigure,
            QtCore.SIGNAL("triggered()"),
            self.configure)

        QtCore.QObject.connect(self.ui.actionEditPost,
            QtCore.SIGNAL("triggered()"),
            self.edit)

        QtCore.QObject.connect(self.ui.actionNewPost,
            QtCore.SIGNAL("triggered()"),
            self.newPost)

        QtCore.QObject.connect(self.ui.actionNew_Story,
            QtCore.SIGNAL("triggered()"),
            self.newStory)

        QtCore.QObject.connect(self.ui.actionRegenerateAll,
            QtCore.SIGNAL("triggered()"),
            self.regenerateAll)

        QtCore.QObject.connect(self.ui.actionRegenerateNeeded,
            QtCore.SIGNAL("triggered()"),
            self.regenerateNeeded)

        QtCore.QObject.connect(self.ui.actionDelete,
            QtCore.SIGNAL("triggered()"),
            self.deletePost)

        QtCore.QObject.connect(self.ui.actionBartleBlog_Help,
            QtCore.SIGNAL("triggered()"),
            self.showHelp)

        self.curPost=None

        self.ui.viewer.document().setDefaultStyleSheet(open("resources/preview.css","r").read())
        self.renderTemplate=None
        
        try:
            self.previewProcess=preview.Preview()
        except:
            QtGui.QMessageBox.warning(self, 'BartleBlog', 
            'Error starting bartleweb.py, previews will not be available.')
            self.previewProcess=None
            
    def showHelp(self):
        self.help=HelpWindow()
        self.help.show()
        
    def deletePost(self):
        if not self.curPost:
            return
        res=QtGui.QMessageBox.question(self,'BartleBlog delete post','Delete post "%s"?'%self.curPost.title,
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if res == QtGui.QMessageBox.Yes:
            self.curPost.destroySelf()
            self.init_tree()

    def about(self):    
        Dialog = QtGui.QDialog()
        ui = BartleBlog.ui.Ui_about.Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.exec_()
        
    def regenerateNeeded(self):
        self.blog.progress=ProgressDialog(self)
        self.blog.progress.show()
        self.blog.regenerate()
        self.blog.progress=None

    def regenerateAll(self):
        self.blog.progress=ProgressDialog(self)
        self.blog.progress.show()
        self.blog.regenerate(all=True)
        self.blog.progress=None

    def edit(self):
        self.editor=EditorWindow(self.curPost, previews=self.previewProcess)
        QtCore.QObject.connect(self.editor,QtCore.SIGNAL('saved'),self.init_tree)
        self.editor.show()

    def newPost(self):
        self.editor=EditorWindow(previews=self.previewProcess)
        QtCore.QObject.connect(self.editor,QtCore.SIGNAL('saved'),self.init_tree)
        self.editor.show()

    def newStory(self):
        self.editor=StoryEditorWindow(previews=self.previewProcess)
        QtCore.QObject.connect(self.editor,QtCore.SIGNAL('saved'),self.init_tree)
        self.editor.show()

    def configure(self, page=None):
        cfg=ConfigWindow(self.blog, page=None)
        cfg.exec_()

    def renderBlog(self):
        self.blog.progress=ProgressDialog(self)
        self.blog.progress.show()
        self.blog.renderBlog()
        self.blog.progress=None

    def renderFullBlog(self):
        self.blog.progress=ProgressDialog(self)
        self.blog.progress.show()
        self.blog.renderFullBlog()
        self.blog.progress=None

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

        if post.is_dirty>1:
            self.reRenderCurrentPost()

        html=Template(self.blog.loadTemplate(self.renderTemplate), output_encoding='utf-8').render(post=post)
        self.ui.viewer.setHtml(html)
        # TODO: give it correct searchpaths so ../static loads thing
        # self.ui.viewer.setSearchPaths(['/home/ralsina/sitio2/stories/'])

    def reRenderCurrentPost(self):
        if self.curPost:
            self.curPost.render()

def main():
    app=QtGui.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    window.init_tree()
    r=app.exec_()
    window.previewProcess.stop()
    sys.exit(r)

def my_excepthook(exc_type, exc_value, exc_traceback):
    app=QtCore.QCoreApplication.instance()
    msg = ' '.join(traceback.format_exception(exc_type,
                                                       exc_value,
                                                       exc_traceback,4))
    QtGui.QMessageBox.critical(None,
                         app.tr("Critical Error"),
                         app.tr("An unexpected Exception has occured!\n"
                                "%1").arg(msg),
                         QtGui.QMessageBox.Ok,
                         QtGui.QMessageBox.NoButton,
                         QtGui.QMessageBox.NoButton)

    # Call the default exception handler if you want
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

def install_handler():
    sys.excepthook = my_excepthook

install_handler()
main()
