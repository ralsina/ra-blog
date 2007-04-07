# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from BartleBlog.ui.Ui_openomy_config import Ui_Form
from BartleBlog.ui.authdialog import AuthDialog
import BartleBlog.backend.dbclasses as db
import BartleBlog.backend.config as config
import BartleBlog.util.openomy as openomy

class OpenomyConfigWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)

        self.setupButtons()
        
        QtCore.QObject.connect(self.ui.get,
            QtCore.SIGNAL("clicked()"),
            self.getToken)
        QtCore.QObject.connect(self.ui.verify,
            QtCore.SIGNAL("clicked()"),
            self.verifyToken)
            
    def setupButtons(self):
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
            t="Token available"
            if config.getValue('openomy','verified','False')=='True':
                t+=' and verified'
            else:
                t+=' but not verified'
            self.ui.status.setText(t)
        
    def getToken(self):
        d=AuthDialog(self,'Enter user and password of your openomy.com account')
        d.exec_()
        op=openomy.Openomy(notoken=True)
        tok=op.Auth_AuthorizeUser(username=str(d.ui.user.text()),
                                  password=str(d.ui.password.text()))
        config.setValue('openomy','token',tok)
        self.setupButtons()

    def verifyToken(self):
        try:
            op=openomy.Openomy()
            op.Files_GetAllFiles(nocache=True)
            config.setValue('openomy','verified','True')
        except openomy.OpenomyError:
            config.setValue('openomy','verified','False')
        self.setupButtons()
            
        
        
