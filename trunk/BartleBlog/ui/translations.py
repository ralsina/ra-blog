# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from BartleBlog.ui.Ui_translations import Ui_Dialog
import BartleBlog.backend.dbclasses as db


class TranslationDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)

        # Set up the UI from designer
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)

