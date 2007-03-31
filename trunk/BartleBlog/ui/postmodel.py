# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from BartleBlog.backend.dbclasses import *
import datetime

class PostModelItem:
    def __init__ (self,parent):
        self._parent=parent
        self.children=[]

    def child (self,row):
        return self.children[row]

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
    def __init__(self,post,parent):
        PostModelItem.__init__(self,parent)
        self.id=post.postID
        self.day=post.pubDate.day
        self.title=post.title

    def rowCount():
        return 0

    def data(self,column):
        if column==0:
            return QtCore.QVariant(str(self.day))
        elif column==1:
            return QtCore.QVariant(str(self.title))
        elif column==2:
            return QtCore.QVariant(str(self.id))
        return QtCore.QVariant()

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
        self.plist=Post.select(AND(Post.q.pubDate>=self.startDate,
                                   Post.q.pubDate<self.endDate),orderBy=Post.q.pubDate)
        self.count=self.plist.count()
        self.children=None

    def data(self,column):
        if column==0:
            return QtCore.QVariant(str(self.month))
        return QtCore.QVariant()

    def childCount(self):
        return self.count

    def child(self,row):
        if not self.children:
            self.children=[PostItem(x,self) for x in self.plist]
        return self.children[row]


class PostYearItem(PostModelItem):
    def __init__(self,year,parent):
        PostModelItem.__init__(self,parent)
        self.year=year
        plist=list(Post.select(AND(Post.q.pubDate>=datetime.datetime(self.year,1,1),
                                   Post.q.pubDate<datetime.datetime(self.year+1,1,1))))
        self.months=[]
        for p in plist:
            if not p.pubDate.month in self.months:
                self.months.append(p.pubDate.month)
        self.months.sort()
        self.children=None

    def child(self,row):
        if not self.children:
            self.children=[PostMonthItem(x,self) for x in self.months]
        return self.children[row]

    def childCount(self):
        return len(self.months)

    def data(self,column):
        if column==0:
            return QtCore.QVariant(str(self.year))
        return QtCore.QVariant()

class PostByDateItem(PostModelItem):
    def __init__(self,parent):
        PostModelItem.__init__(self,parent)
        plist=Post.select(orderBy=Post.q.pubDate)
        y1=plist[0].pubDate.replace(day=1,month=1)
        y2=plist[-1].pubDate
        y2=y2.replace(year=y2.year+1,day=1,month=1)
        self.children=None
        self.years=[]
        for yy in xrange(y1.year,y2.year):
            yb=y1.replace(year=yy)
            ye=y1.replace(year=yy+1)
            if Post.select(AND(Post.q.pubDate>=yb,Post.q.pubDate<ye)).count():
                self.years.append(yy)
        self.years.sort()

    def childCount(self):
        return len(self.years)

    def child(self,row):
        if not self.children:
            self.children=[PostYearItem(x,self) for x in self.years]
        return self.children[row]

    def data(self,column):
        if column==0:
            return QtCore.QVariant("Posts by Date")
        return QtCore.QVariant()

class StoryItem(PostModelItem):
    def __init__(self,story,parent):
        PostModelItem.__init__(self,parent)
        self.id=story.postID
        self.title=story.title
    def data(self,column):
        if column==0:
            return QtCore.QVariant(str(self.id))
        elif column==1:
            return QtCore.QVariant(str(self.title))
        return QtCore.QVariant()

class StoriesItem(PostModelItem):
    def __init__(self,parent):
        PostModelItem.__init__(self,parent)
        self.children=None

    def child(self,row):
        if not self.children:
            self.children=[StoryItem(x,self) for x in list(Story.select())]
        return self.children[row]

    def childCount(self):
        return Story.select().count()

    def data(self,column):
        if column==0:
            return QtCore.QVariant("Stories")
        return QtCore.QVariant()


class PostModel(QtCore.QAbstractItemModel):
    def __init__(self,parent=None):
        QtCore.QAbstractItemModel.__init__(self,parent)
        self.rootItem=PostModelItem(None)
        self.rootItem.appendChild(PostByDateItem(self.rootItem))
        self.rootItem.appendChild(StoriesItem(self.rootItem))
        self.columns=["","Title"]

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
