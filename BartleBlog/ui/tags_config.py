# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from BartleBlog.ui.Ui_tags_config import Ui_Form

class TagsConfigWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        
        

