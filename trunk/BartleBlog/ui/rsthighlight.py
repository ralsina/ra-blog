# -*- coding: utf-8 -*-

from PyQt import QtGui

class rstHighlighter (QtGui.QSyntaxHighlighter):
    def __init__(self):
        QtGui.QSyntaxHighlighter.__init__(self)
