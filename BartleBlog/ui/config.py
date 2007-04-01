# -*- coding: utf-8 -*-

from BartleBlog.ui.Ui_main_config import Ui_Dialog

class ConfigWindow(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        # Set up the UI from designer
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
