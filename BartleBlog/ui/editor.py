# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import time

from BartleBlog.ui.Ui_rsteditor import Ui_MainWindow
import BartleBlog.backend.dbclasses as db

class EditorWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Set up the UI from designer
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.post=None
        
        QtCore.QObject.connect(self.ui.actionSave,
            QtCore.SIGNAL("triggered()"),
            self.savePost)
        
        
    def savePost(self):
        if not self.post:
            self.post=db.Post( postID="BB%s"+str(time.time()),
                            title=str(self.ui.title.text()),
                            link=str(self.ui.link.text()),
                            text=str(self.ui.editor.toPlainText()))
            # Silly hack to have PostID be unique but not ugly
            self.post.PostID='BB'+str(self.post.id)
            
            self.emit(QtCore.SIGNAL('saved'))

        
