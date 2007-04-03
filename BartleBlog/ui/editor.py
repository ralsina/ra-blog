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
        
    def closeWindow(self):
        self.close()
        
    def setPost(self,post):
        self.post=post
        if not post:
            return
            
        self.ui.title.setText(post.title)
        self.ui.link.setText(post.link)
        self.ui.editor.setText(post.text)

        
    def savePost(self):
        if not self.post:
            self.post=db.Post( postID="BB%s"%str(time.time()),
                            title=str(self.ui.title.text()),
                            link=str(self.ui.link.text()),
                            text=str(self.ui.editor.toPlainText()))
            # Silly hack to have PostID be unique but not ugly
            self.post.PostID='BB'+str(self.post.id)
        else:
            self.post.title=str(self.ui.title.text())
            self.post.link=str(self.ui.link.text())
            self.post.text=str(self.ui.editor.toPlainText())
            self.post.is_dirty=True
        self.emit(QtCore.SIGNAL('saved'))

        