# -*- coding: utf-8 -*-

from PyQt4 import QtGui

class rstHighlighter (QtGui.QSyntaxHighlighter):
    def __init__(self,document):
        QtGui.QSyntaxHighlighter.__init__(self,document)

        
    def highlightBlock(self,text):
        pass
