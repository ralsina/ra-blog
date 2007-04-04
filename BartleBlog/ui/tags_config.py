# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from BartleBlog.ui.Ui_tags_config import Ui_Form
import BartleBlog.backend.dbclasses as db


class TagsConfigWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.curTag=None

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        
        self.loadTags()
        QtCore.QObject.connect(self.ui.list,QtCore.SIGNAL('activated(QString)'),
            self.loadTag)
            
        
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
            self.saveTag()
            self.curTag=db.Category.select(db.Category.q.name==str(tagname))[0]
            if self.curTag.title:
                self.ui.title.setText(self.curTag.title)
            if self.curTag.magicWords:
                self.ui.magicWords.setText(self.curTag.magicWords)
            if self.curTag.description:
                self.ui.description.setText(self.curTag.description)
        
        

