#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
from Ui_mainwindow import Ui_MainWindow
from sqlobject import *
import os
from dbclasses import *
import datetime
import docutils.core

class PostModelItem:
    def __init__ (self,parent):
        self._parent=parent
        self.children=[]
        
    def child (self,row):
        pass
        
    def childCount(self):
        return len(self.children)
        
    def columnCount(self):
        return 1
        
    def data(self,column):
        throw ("Implement data in the child class")        
        
    def row(self):
        if self.parent:
            return self._parent.children.index(self)
        return 0
        
    def parent(self):
        return self._parent
        
    def appendChild(self,item):
        self.children.append(item)

    def child(self,row):
        return self.children[row]

class PostItem(PostModelItem):
    def __init__(self,id,parent):
        PostModelItem.__init__(self,parent)
        self.id=id        
        self.title=None
    def data(self,column):
        if column==0:
            return QtCore.QVariant(str(self.id))
        elif column==1:
            if not self.title:
                self.title=list(Post.select(Post.q.postID==self.id))[0].title
            return QtCore.QVariant(str(self.title))
        return QtCore.QVariant()
    
class PostDayItem(PostModelItem):
    def __init__(self,day,parent):
        PostModelItem.__init__(self,parent)
        self.month=day
        self.children={}
        self.startDate=datetime.datetime(parent.parent().year,parent.month,day)
        try:
            self.endDate=datetime.datetime(parent.parent().year,parent.month,day+1)
        except:
            try:
                self.endDate=datetime.datetime(parent.parent().year,parent.month+1,1)
            except:
                self.endDate=datetime.datetime(parent.parent().year+1,1,1)
        self.plist=list(Post.select(AND(Post.q.pubDate>=self.startDate,
                                   Post.q.pubDate<self.endDate)))
        
    def data(self,column):
        if column==0:
            return QtCore.QVariant(str(self.month))
        return QtCore.QVariant()
        
    def childCount(self):
        return len(self.plist)
        
    def child(self,row):
        if not self.children.has_key(row):
            self.children[row]=PostItem(self.plist[row].postID,self)
        return self.children[row]
        
class PostMonthItem(PostModelItem):
    def __init__(self,month,parent):
        PostModelItem.__init__(self,parent)
        self.month=month
        days=[]        
        self.startDate=datetime.datetime(parent.year,month,1)
        if month==12:
            self.endDate=datetime.datetime(parent.year+1,1,1)
        else:
            self.endDate=datetime.datetime(parent.year,month+1,1)
        plist=list(Post.select(AND(Post.q.pubDate>=self.startDate,
                                   Post.q.pubDate<self.endDate)))
                                   
        for p in plist:
            if not p.pubDate.day in days:
                days.append(p.pubDate.day)
        days.sort()
        self.children=[PostDayItem(x,self) for x in days]
        
    def data(self,column):
        if column==0:
            return QtCore.QVariant(str(self.month))
        return QtCore.QVariant()
        
        
class PostYearItem(PostModelItem):
    def __init__(self,year,parent):
        PostModelItem.__init__(self,parent)        
        self.year=year
        plist=list(Post.select(AND(Post.q.pubDate>=datetime.datetime(self.year,1,1),
                                   Post.q.pubDate<datetime.datetime(self.year+1,1,1))))
        months=[]
        for p in plist:
            if not p.pubDate.month in months:
                months.append(p.pubDate.month)
        months.sort()
        self.children=[PostMonthItem(x,self) for x in months]
        
    def data(self,column):
        if column==0:
            return QtCore.QVariant(str(self.year))
        return QtCore.QVariant()
                
class PostByDateItem(PostModelItem):
    def __init__(self,parent):
        PostModelItem.__init__(self,parent)
        plist=list(Post.select())
        self.children=[]
        self.years=[]
        for p in plist:
            if not p.pubDate.year in self.years:
                self.children.append(PostYearItem(p.pubDate.year,self))
                self.years.append(p.pubDate.year)
                    
    def data(self,column):
        print "data",column
        if column==0:
            return QtCore.QVariant("Posts by Date")
        return QtCore.QVariant()        

class PostModel(QtCore.QAbstractItemModel):
    def __init__(self,parent=None):
        QtCore.QAbstractItemModel.__init__(self,parent)
        self.rootItem=PostByDateItem(None)
        self.columns=["Posts","Title"]

    def index (self,row,column,parentIndex):
        if not parentIndex.isValid():
            parentItem=self.rootItem
        else:
            parentItem=parentIndex.internalPointer()
        childItem=parentItem.child(row)
        if childItem:
            return self.createIndex(row,column,childItem)
        return QtCore.QModelIndex()
        
    def parent(self,index):
        if not index.isValid():
            return QtCore.QModelIndex()
        childItem=index.internalPointer()
        parentItem=childItem.parent()
        if parentItem == self.rootItem:
            return QtCore.QModelIndex()
        return self.createIndex(parentItem.row(),0,parentItem)
        
    def rowCount(self,parent):
        if not parent.isValid():
            parentItem=self.rootItem
        else:
            parentItem=parent.internalPointer()
        return parentItem.childCount()
    
    def columnCount(self,parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        return len(self.columns)
        
    def data(self,index,role):
        if not index.isValid():
            return QtCore.QVariant()
        if role <> QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        treeitem=index.internalPointer()
        return treeitem.data(index.column())
        
    def flags(self,index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
    def headerData(self,section,orientation,role):
        if orientation==QtCore.Qt.Horizontal and \
           role == QtCore.Qt.DisplayRole:
           
            res=QtCore.QVariant(self.columns[section])
        else:
            res=QtCore.QVariant()
        return res
        
    

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # Set up the UI from designer
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        db_fname=os.path.abspath('blog.db')
        connection_string='sqlite:'+db_fname
        connection=connectionForURI(connection_string)
        sqlhub.processConnection = connection
        self.model=PostModel()
        
        self.ui.actionEdit_Item.setCheckable(True)
        
        QtCore.QObject.connect(self.ui.tree,
            QtCore.SIGNAL("activated(QModelIndex)"),
            self.openItem)
            
        QtCore.QObject.connect(self.ui.actionEdit_Item,
            QtCore.SIGNAL("toggled(bool)"),
            self.switchEditMode)

        self.ui.stack.setCurrentIndex(0)
        self.curPost=None

    def init_tree(self):
        self.ui.tree.setModel(self.model)
        
    def openItem(self,index):
        try:
            treeitem=index.internalPointer()
        except:
            pass
        if self.ui.editor.document().isModified():
            self.reRenderCurrentPost()

        try:
            self.curPost=list(Post.select(Post.q.postID==treeitem.id))[0]        
            self.ui.editor.setText(self.curPost.text)
            self.ui.editor.document().setModified(False)
            self.ui.viewer.setHtml(self.curPost.rendered)
            self.ui.title.setText(self.curPost.title)
            self.ui.link.setText(self.curPost.link)
            self.ui.categories.setText(','.join([x.nameID for x in self.curPost.categories]))
            self.switchEditMode(self.ui.actionEdit_Item.isChecked())
        except AttributeError:
            pass
        
        
    def reRenderCurrentPost(self):
        if self.curPost:
            print "Rerendering ",self.curPost.postID
            self.curPost.text=str(self.ui.editor.document().toPlainText())
            html=docutils.core.publish_parts(self.curPost.text,writer_name='html')['body']
            self.ui.viewer.setHtml(html)
            self.curPost.rendered=html
                    
    def switchEditMode(self,mode):
        if mode==1:
            self.ui.stack.setCurrentIndex(1)
            self.ui.editor.setFocus()
        else:
            self.ui.stack.setCurrentIndex(0)
            if self.ui.editor.document().isModified():
                self.reRenderCurrentPost()
            self.ui.viewer.setFocus()
        
def main():
    app=QtGui.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    window.init_tree()
    print window.model.columnCount(window.ui.tree.rootIndex())
    sys.exit(app.exec_())
    
main()
