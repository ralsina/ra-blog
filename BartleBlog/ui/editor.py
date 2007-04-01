# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from BartleBlog.ui.Ui_rsteditor import Ui_MainWindow

class EditorWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Set up the UI from designer
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
