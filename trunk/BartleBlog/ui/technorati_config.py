# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from BartleBlog.ui.Ui_technorati_config import Ui_Form
import os
import BartleBlog.backend.config as config

class TechnoratiConfigWidget(QtGui.QWidget):
    def __init__(self,blog, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.blog=blog

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)
