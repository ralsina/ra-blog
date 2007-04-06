# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from BartleBlog.ui.Ui_openomy_config import Ui_Form
import BartleBlog.backend.dbclasses as db
import BartleBlog.backend.config as config
import BartleBlog.util.openomy as openomy

class OpenomyConfigWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)

        self.tok=config.getValue('openomy','token')
        if not self.tok:
            self.ui.forget.setEnabled(False)
            self.ui.verify.setEnabled(False)
            self.ui.get.setEnabled(True)
            self.ui.status.setText("No token available")
            
        else:        
            self.ui.forget.setEnabled(True)
            self.ui.verify.setEnabled(True)
            self.ui.get.setEnabled(False)
            self.ui.status.setText("Token available")
        
