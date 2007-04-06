# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import time

from BartleBlog.ui.Ui_rsteditor import Ui_MainWindow
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
                            title=str(self.ui.title.text()),
                            link=str(self.ui.link.text()),
                            text=str(self.ui.editor.toPlainText()))
            # Silly hack to have PostID be unique but not ugly
            self.post.postID='BB'+str(self.post.id)
        else:
            self.post.title=str(self.ui.title.text())
            self.post.link=str(self.ui.link.text())
            self.post.text=str(self.ui.editor.toPlainText())
            self.post.render()
            
        cats=[ db.Category.select(db.Category.q.name==c)[0] for c in \
                unicode(self.ui.tags.text()).split(',') ]
        self.post.setCategories(cats)
        self.post.is_dirty=99
        self.emit(QtCore.SIGNAL('saved'))

        
