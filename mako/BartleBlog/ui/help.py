# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import codecs

from BartleBlog.ui.Ui_help import Ui_MainWindow

class HelpWindow(QtGui.QMainWindow):
    def __init__(self,post=None):
        QtGui.QMainWindow.__init__(self)

        # Set up the UI from designer
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.view.setHtml(codecs.open('resources/help.html', 'r', 'utf-8').read())
        
