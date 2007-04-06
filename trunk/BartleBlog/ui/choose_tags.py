# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from Ui_choose_tags import Ui_Dialog
import BartleBlog.backend.dbclasses as db


class TagsDialog(QtGui.QDialog):
    def __init__(self,parent=None,selected=''):
        QtGui.QWidget.__init__(self,parent)
        
        # Set up the UI from designer
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.selected=selected.split(',')
        
        for c in db.Category.select():
            item=QtGui.QListWidgetItem(c.name,self.ui.list)
            if c.name in selected:
                item.setSelected(True)
                
        QtCore.QObject.connect(self.ui.list,
            QtCore.SIGNAL("currentTextChanged ( const QString &) "),
            self.showCategory)
            
    def showCategory(self,text):
        text=unicode(text)
        cat=db.Category.select(db.Category.q.name==text)[0]
        self.ui.text.setHtml('<h3>%s</h3>%s'%(cat.title,cat.description))
        

    def currentCategories(self):
        return ','.join( [unicode(x.text()) for x in  self.ui.list.selectedItems()])
