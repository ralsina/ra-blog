# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from BartleBlog.ui.Ui_menu_config import Ui_Form
import BartleBlog.backend.config as config
from BartleBlog.util.demjson import JSON

class MenuConfigWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        
        self.menu=config.getValue('blog', 'menu')
        self.ui.extra_data.setVisible(False)
        
        QtCore.QObject.connect(self.ui.new,
            QtCore.SIGNAL("clicked()"),
            self.newItem)
            
        QtCore.QObject.connect(self.ui.tree, 
            QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'), 
            self.editItem)
            
        QtCore.QObject.connect(self.ui.label, 
            QtCore.SIGNAL('textChanged(QString)'), 
            self.labelChanged)
            
        QtCore.QObject.connect(self.ui.right, 
            QtCore.SIGNAL('clicked()'), 
            self.moveRight)
            
        QtCore.QObject.connect(self.ui.left,  
            QtCore.SIGNAL('clicked()'), 
            self.moveLeft)

        QtCore.QObject.connect(self.ui.up,  
            QtCore.SIGNAL('clicked()'), 
            self.moveUp)

        QtCore.QObject.connect(self.ui.down,  
            QtCore.SIGNAL('clicked()'), 
            self.moveDown)

        QtCore.QObject.connect(self.ui.delete,  
            QtCore.SIGNAL('clicked()'), 
            self.delete)

        QtCore.QObject.connect(self.ui.save,  
            QtCore.SIGNAL('clicked()'), 
            self.save)

        self.load()
        
    def load(self):
        data=JSON().decode(config.getValue('blog', 'menu', "[]"))
        print data        
        for item in data:
            print item
            i=QtGui.QTreeWidgetItem([item[0]])
            i.extra_type=item[1] 
            i.extra_data=item[2]
            self.ui.tree.addTopLevelItem(i)
            for subi in item[3]:
                si=QtGui.QTreeWidgetItem([subi[0]])
                si.extra_type=subi[1] 
                si.extra_data=subi[2]
                i.addChild(si)

    def process(self, item):
        data=[]
        for i in range(0, item.childCount()):
            child=item.child(i)
            data.append([unicode(child.text(0)), child.extra_type, child.extra_data])
        return data
    def save(self):
        data=[]
        for i in range(0, self.ui.tree.topLevelItemCount()):
            item=self.ui.tree.topLevelItem(i)
            data.append([unicode(item.text(0)), item.extra_type, item.extra_data, self.process(item)])
        config.setValue('blog', 'menu',JSON().encode(data) )

    def delete(self):
        i=self.ui.tree.currentItem()
        if not i:
            return
        p=i.parent()
        if p:
            p.takeChild(p.indexOfChild(i))
        else:
            self.ui.tree.takeTopLevelItem(self.ui.tree.indexOfTopLevelItem(i))

    def moveUp(self):
        i=self.ui.tree.currentItem()
        if not i:
            return
        p=i.parent()
        if p:
            index=p.indexOfChild(i)
            p.takeChild(index)
            p.insertChild(index-1, i)
            p.setExpanded(True)
        else:
            index=self.ui.tree.indexOfTopLevelItem(i)
            self.ui.tree.takeTopLevelItem(index)
            self.ui.tree.insertTopLevelItem(index-1, i)            
        self.ui.tree.setCurrentItem(i)
        self.editItem(i)
        
    def moveDown(self):
        i=self.ui.tree.currentItem()
        if not i:
            return
        p=i.parent()
        if p:
            index=p.indexOfChild(i)
            p.takeChild(index)
            p.insertChild(index+1, i)
            p.setExpanded(True)
        else:
            index=self.ui.tree.indexOfTopLevelItem(i)
            self.ui.tree.takeTopLevelItem(index)
            self.ui.tree.insertTopLevelItem(index+1, i)
        self.ui.tree.setCurrentItem(i)
        self.editItem(i)

    def moveRight(self):
        i=self.ui.tree.currentItem()
        if not i:
            return
        p=i.parent()
        if p:
            index=p.indexOfChild(i)
            p.takeChild(index)
            p.child(index-1).addChild(i)
            p.setExpanded(True)
        else:
            index=self.ui.tree.indexOfTopLevelItem(i)
            self.ui.tree.takeTopLevelItem(index)
            self.ui.tree.topLevelItem(index-1).addChild(i)            
            self.ui.tree.topLevelItem(index-1).setExpanded(True)
        self.ui.tree.setCurrentItem(i)
        self.editItem(i)
        
    def moveLeft(self):
        i=self.ui.tree.currentItem()
        if not i:
            return
        p=i.parent()
        if not p:
            return
        g=p.parent()
        p.takeChild(p.indexOfChild(i))        
        if g:
            g.insertChild(g.indexOfChild(p)+1, i)            
        else:
            self.ui.tree.insertTopLevelItem(self.ui.tree.indexOfTopLevelItem(p)+1, i)
            
        p.setExpanded(True)
        self.ui.tree.setCurrentItem(i)
        self.editItem(i)
        
    def labelChanged(self, text):
        i=self.ui.tree.currentItem()
        if i:
            i.setText(0,text)

    def enableButtons(self):
        print 'enableButtons'
        i=self.ui.tree.currentItem()
        self.ui.left.setEnabled(False)
        self.ui.right.setEnabled(False)
        self.ui.up.setEnabled(False)
        self.ui.down.setEnabled(False)
        if not i:
            return
        self.ui.delete.setEnabled(True)
        if i.parent():
            self.ui.left.setEnabled(True)
            if i.parent().indexOfChild(i)>0:
                self.ui.up.setEnabled(True)
            if self.ui.tree.indexOfTopLevelItem(i)<i.parent().childCount()-1:
                self.ui.down.setEnabled(True)
            if i.parent().childCount()>1:
                if i.parent().indexOfChild(i)>0 and not i.parent().parent():
                    self.ui.right.setEnabled(True)
        else:
            if self.ui.tree.topLevelItemCount()>1:
                if self.ui.tree.indexOfTopLevelItem(i)>0:
                    self.ui.right.setEnabled(True)
            if self.ui.tree.indexOfTopLevelItem(i)>0:
                self.ui.up.setEnabled(True)
            if self.ui.tree.indexOfTopLevelItem(i)<self.ui.tree.topLevelItemCount()-1:
                self.ui.down.setEnabled(True)
            
    def editItem(self, item,  col=0):
        print 'editItem'
        self.enableButtons()
        t=unicode(item.text(0))
        self.ui.label.setText(t.lstrip())
        self.ui.label.setFocus()
        if item.extra_type=='label':
            self.ui.data_type.setText('')
            self.ui.extra_data.setVisible(False)
            self.ui.type.setCurrentIndex(1)
            
    def newItem(self):
        item=QtGui.QTreeWidgetItem(['New Item'])
        i=self.ui.tree.currentItem()
        p=None
        if i:
            p=i.parent()
        if p:
            p.addChild(item)
        else:
            self.ui.tree.addTopLevelItem(item)
        item.extra_data=''
        item.extra_type='label'
        self.ui.tree.setCurrentItem(item)
        self.editItem(item)
        
