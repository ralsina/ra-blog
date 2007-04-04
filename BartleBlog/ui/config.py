# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from BartleBlog.ui.Ui_main_config import Ui_Dialog

from BartleBlog.ui.tags_config import TagsConfigWidget

class ConfigWindow(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        # Set up the UI from designer
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        
        # Add configuration items to the list
        
        QtGui.QListWidgetItem("Tags",self.ui.list)
        self.widgets={}
        self.widgets['tags']=TagsConfigWidget()
        self.layout=QtGui.QHBoxLayout()
        self.layout.addWidget(self.widgets['tags'])
        self.ui.frame.setLayout(self.layout)
        
        
        
        
