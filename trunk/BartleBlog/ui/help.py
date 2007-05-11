# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from BartleBlog.ui.Ui_help import Ui_MainWindow
import BartleBlog.help as help

class HelpWindow(QtGui.QMainWindow):
    def __init__(self,post=None):
        QtGui.QMainWindow.__init__(self)

        # Set up the UI from designer
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        print 'aaaa'
        f=QtCore.QFile(':/help/help/help.rst')
        print f.readAll()
        
        
