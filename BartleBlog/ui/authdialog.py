# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from Ui_authdialog import Ui_Dialog
import BartleBlog.backend.dbclasses as db


class AuthDialog(QtGui.QDialog):
    def __init__(self,parent=None,text='Please enter user and password:'):
        QtGui.QWidget.__init__(self,parent)
        
        # Set up the UI from designer
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.message.setText(text)

