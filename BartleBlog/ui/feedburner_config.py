# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from BartleBlog.ui.Ui_feedburner_config import Ui_Form
from BartleBlog.backend import config
from BartleBlog.util.feedburner import Management

class FeedBurnerConfigWidget(QtGui.QWidget):
    def __init__(self, blog, parent=None):
        QtGui.QWidget.__init__(self,parent)

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.password.setText(config.getValue("feedburner", "password", ""))
        self.ui.username.setText(config.getValue("feedburner", "username", ""))
        self.ui.enabled.setChecked(config.getValue("feedburner", "enabled", False))

        QtCore.QObject.connect(self.ui.username,QtCore.SIGNAL('textChanged(QString)'),
            self.save)
        QtCore.QObject.connect(self.ui.password,QtCore.SIGNAL('textChanged(QString)'),
            self.save)
        QtCore.QObject.connect(self.ui.enabled,QtCore.SIGNAL('toggled(bool)'),
            self.save)
        
    def save(self):
      if self.ui.enabled.isChecked():
        config.setValue("feedburner", "enabled", True)
        config.setValue("feedburner", "password", unicode(self.ui.password.text()))
        config.setValue("feedburner", "username", unicode(self.ui.username.text()))
      else:
        config.setValue("feedburner", "enabled", False)
        config.setValue("feedburner", "password", "")
        config.setValue("feedburner", "username", "")
