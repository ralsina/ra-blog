# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from BartleBlog.ui.Ui_blog_config import Ui_Form

import BartleBlog.backend.config as config

class BlogConfigWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)

