# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from BartleBlog.ui.Ui_blog_config import Ui_Form
import os
import BartleBlog.backend.config as config

class BlogConfigWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.save,
            QtCore.SIGNAL("clicked()"),
            self.save)
            
        self.ui.title.setText(config.getValue('blog', 'title', 'My First Blog'))
        self.ui.url.setText(config.getValue('blog', 'url', 'http://'))
        self.ui.author.setText(config.getValue('blog', 'author', 'Joe Doe'))
        self.ui.email.setText(config.getValue('blog', 'email', 'joe@doe'))
        self.ui.folder.setText(config.getValue('blog', 'folder', os.path.expanduser("~/.bartleblog/weblog")))
        self.ui.description.setPlainText(config.getValue('blog', 'description', 'My Blog'))
            
    def save(self):
        config.setValue('blog','title', unicode(self.ui.title.text()))
        config.setValue('blog','url', unicode(self.ui.url.text()))
        config.setValue('blog','author', unicode(self.ui.author.text()))
        config.setValue('blog','email', unicode(self.ui.email.text()))
        config.setValue('blog','folder', unicode(self.ui.folder.text()))
        config.setValue('blog','description', unicode(self.ui.description.toPlainText()))
