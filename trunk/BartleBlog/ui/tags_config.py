# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from BartleBlog.ui.Ui_tags_config import Ui_Form
import BartleBlog.backend.dbclasses as db


class TagsConfigWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        
        self.loadTags()
        QtCore.QObject.connect(self.ui.list,QtCore.SIGNAL('activated(QString)'),
            self.loadTag)
        
            
    def loadTags(self):
        self.ui.list.clear()
        for tag in db.Category.select(orderBy=db.Category.q.name):
            self.ui.list.addItem(tag.name)
        self.loadTag(self.ui.list.itemText(0))
            
    def loadTag(self,tagname):
            tag=db.Category.select(db.Category.q.name==str(tagname))[0]
            if tag.title:
                self.ui.title.setText(tag.title)
            if tag.magicWords:
                self.ui.magicWords.setText(tag.magicWords)
            if tag.description:
                self.ui.description.setText(tag.description)
        
        

