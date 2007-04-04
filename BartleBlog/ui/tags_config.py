# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from BartleBlog.ui.Ui_tags_config import Ui_Form
import BartleBlog.backend.dbclasses as db


class TagsConfigWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.curTag=None
        self.newName=None
        
        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        
        self.loadTags()
        QtCore.QObject.connect(self.ui.list,QtCore.SIGNAL('activated(QString)'),
            self.loadTag)
        QtCore.QObject.connect(self.ui.new,QtCore.SIGNAL('clicked()'),
            self.newTag)
        QtCore.QObject.connect(self.ui.delete,QtCore.SIGNAL('clicked()'),
            self.delTag)
        QtCore.QObject.connect(self.ui.rename,QtCore.SIGNAL('clicked()'),
            self.renameTag)
    
    def renameTag(self):
        text,ok=QtGui.QInputDialog.getText(self,'BartleBlog - Rename Tag','Enter the new name of the %s tag'%self.curTag.name)
        text=str(text)
        if ok:
            self.curTag.name=text
            self.loadTags()
            self.loadTag(text)
            self.ui.list.setCurrentIndex(self.ui.list.findText(text))
    
    def delTag(self):
        res=QtGui.QMessageBox.question(self,'BartleBlog delete tag','Delete tag %s?'%self.curTag.name,
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if res == QtGui.QMessageBox.Yes:
            self.curTag.destroySelf()
            self.loadTags()
        
    def fillWidgets(self):
        self.ui.title.setText('')
        self.ui.magicWords.setText('')
        self.ui.description.setText('')
        if self.curTag.title:
            self.ui.title.setText(self.curTag.title)
        if self.curTag.magicWords:
            self.ui.magicWords.setText(self.curTag.magicWords)
        if self.curTag.description:
            self.ui.description.setText(self.curTag.description)
        
    def newTag(self):
        text,ok=QtGui.QInputDialog.getText(self,'BartleBlog - New Tag','Enter the name of the new tag')
        text=str(text)
        if ok:
            self.curTag=db.Category(name=text,description='Posts about %s'%text,title=text,magicWords=text)
            self.fillWidgets()
            self.loadTags()
            self.loadTag(text)
            self.ui.list.setCurrentIndex(self.ui.list.findText(text))
            
        
        
    def saveTag(self):
        if not self.curTag:
            return
        self.curTag.description=str(self.ui.description.toPlainText())
        self.curTag.title=str(self.ui.title.text())
        self.curTag.magicWords=str(self.ui.magicWords.text())
        
    def loadTags(self):
        self.ui.list.clear()
        for tag in db.Category.select(orderBy=db.Category.q.name):
            self.ui.list.addItem(tag.name)
        self.loadTag(self.ui.list.itemText(0))
            
    def loadTag(self,tagname):
        self.newName=None
        self.saveTag()
        self.curTag=db.Category.select(db.Category.q.name==str(tagname))[0]
        self.fillWidgets()
