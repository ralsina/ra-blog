# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import time

from BartleBlog.ui.Ui_rsteditor import Ui_MainWindow
from BartleBlog.ui.choose_tags import TagsDialog
import BartleBlog.backend.dbclasses as db


class EditorWindow(QtGui.QMainWindow):
    def __init__(self,post=None):
        QtGui.QMainWindow.__init__(self)

        # Set up the UI from designer
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setPost(post)

        QtCore.QObject.connect(self.ui.actionSave,
            QtCore.SIGNAL("triggered()"),
            self.savePost)

        QtCore.QObject.connect(self.ui.actionClose,
            QtCore.SIGNAL("triggered()"),
            self.closeWindow)

        QtCore.QObject.connect(self.ui.guess,
            QtCore.SIGNAL("clicked()"),
            self.guessTags)

        QtCore.QObject.connect(self.ui.tags,
            QtCore.SIGNAL("clicked()"),
            self.chooseTags)

    def chooseTags(self):
        self.d=TagsDialog(self,self.ui.tags.text())
        r=self.d.exec_()

        if r:
            self.ui.tags.setText(self.d.currentCategories())
        del self.d

    def guessTags(self):
        self.ui.tags.setText(','.join(db.guessCategories(unicode(self.ui.editor.toPlainText())+unicode(self.ui.title.text()))))

    def closeWindow(self):
        self.close()

    def setPost(self,post):
        self.post=post
        if not post:
            return

        self.ui.title.setText(post.title)
        self.ui.link.setText(post.link)
        self.ui.editor.setPlainText(post.text)
        self.ui.tags.setText(','.join( [c.name for c in post.categories]))


    def savePost(self):
        if not self.post:
            self.post=db.Post( postID="BB%s"%str(time.time()),
                            title=unicode(self.ui.title.text()),
                            link=unicode(self.ui.link.text()),
                            text=unicode(self.ui.editor.toPlainText()))
            # Silly hack to have PostID be unique but not ugly
            self.post.postID='BB'+str(self.post.id)
        else:
            self.post.title=str(self.ui.title.text())
            self.post.link=str(self.ui.link.text())
            self.post.text=str(self.ui.editor.toPlainText())
            self.post.render()
        t=unicode(self.ui.tags.text())
        if t:
            cats=[ db.Category.select(db.Category.q.name==c)[0] for c in \
                t.split(',') ]
            self.post.setCategories(cats)
        self.post.render()
        self.post.setDirtyPages()
        self.emit(QtCore.SIGNAL('saved'))
