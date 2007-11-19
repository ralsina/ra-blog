# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from BartleBlog.ui.Ui_translation_config import Ui_Form
import BartleBlog.backend.dbclasses as db


class TranslationConfigWidget(QtGui.QWidget):
    def __init__(self, blog, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.curTag=None
        self.newName=None

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        
        self.loadTranslations()

        QtCore.QObject.connect(self.ui.new,QtCore.SIGNAL('clicked()'),
            self.newTranslation)

        QtCore.QObject.connect(self.ui.delete,QtCore.SIGNAL('clicked()'),
            self.delTranslation)

    def delTranslation(self):
        print "CT ", self.curTranslation()
        if not self.curTranslation():
            return
        res=QtGui.QMessageBox.question(self,'BartleBlog delete translation','Delete translation %s?'%self.curTranslation().name,
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if res == QtGui.QMessageBox.Yes:
            self.curTranslation().destroySelf()
            self.loadTranslations()


    def loadTranslations(self):
        self.ui.list.clear()
        for t in db.Translation.select(orderBy=db.Translation.q.name):
            self.ui.list.addItem(t.name)
                   
    def newTranslation(self):
        text,ok=QtGui.QInputDialog.getText(self,'BartleBlog - New Translation','Enter the name of the new translation')
        text=str(text)
        if ok:
            trans=db.Translation(name=text)
            self.loadTranslations()


    def curTranslation(self):
        l=self.ui.list.selectedItems()
        print "L: ", l
        if not l:
            return None
        sel=db.Translation.select(db.Translation.q.name==str(l[0].text()))
        if sel.count()>0:
            return list(sel)[0]
        return None
