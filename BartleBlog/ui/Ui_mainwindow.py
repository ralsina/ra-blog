# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/ra-blog/bartleblog/BartleBlog/ui/mainwindow.ui'
#
# Created: Wed Apr  4 21:15:26 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,686,552).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.tree = QtGui.QTreeView(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree.sizePolicy().hasHeightForWidth())
        self.tree.setSizePolicy(sizePolicy)
        self.tree.setSortingEnabled(False)
        self.tree.setAnimated(False)
        self.tree.setAllColumnsShowFocus(True)
        self.tree.setObjectName("tree")

        self.stack = QtGui.QStackedWidget(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stack.sizePolicy().hasHeightForWidth())
        self.stack.setSizePolicy(sizePolicy)
        self.stack.setObjectName("stack")

        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.page_2)
        self.hboxlayout1.setMargin(9)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.viewer = QtGui.QTextBrowser(self.page_2)
        self.viewer.setOpenExternalLinks(True)
        self.viewer.setObjectName("viewer")
        self.hboxlayout1.addWidget(self.viewer)
        self.stack.addWidget(self.page_2)

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.vboxlayout = QtGui.QVBoxLayout(self.page)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(self.page)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.link = QtGui.QLineEdit(self.page)
        self.link.setObjectName("link")
        self.gridlayout.addWidget(self.link,1,1,1,1)

        self.label_2 = QtGui.QLabel(self.page)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.title = QtGui.QLineEdit(self.page)
        self.title.setObjectName("title")
        self.gridlayout.addWidget(self.title,0,1,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.editor = QtGui.QTextEdit(self.page)
        self.editor.setObjectName("editor")
        self.vboxlayout.addWidget(self.editor)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.categories = QtGui.QLineEdit(self.page)
        self.categories.setObjectName("categories")
        self.hboxlayout2.addWidget(self.categories)

        self.pubDate = QtGui.QDateTimeEdit(self.page)
        self.pubDate.setObjectName("pubDate")
        self.hboxlayout2.addWidget(self.pubDate)
        self.vboxlayout.addLayout(self.hboxlayout2)
        self.stack.addWidget(self.page)
        self.hboxlayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,686,31))
        self.menubar.setObjectName("menubar")

        self.menu_Post = QtGui.QMenu(self.menubar)
        self.menu_Post.setObjectName("menu_Post")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")

        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")

        self.menuBlog = QtGui.QMenu(self.menubar)
        self.menuBlog.setObjectName("menuBlog")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(self.toolBar)

        self.actionEditPost = QtGui.QAction(MainWindow)
        self.actionEditPost.setCheckable(False)
        self.actionEditPost.setIcon(QtGui.QIcon(":/icons/icons/edit.png"))
        self.actionEditPost.setObjectName("actionEditPost")

        self.actionRender_Blog = QtGui.QAction(MainWindow)
        self.actionRender_Blog.setIcon(QtGui.QIcon(":/icons/icons/up.png"))
        self.actionRender_Blog.setObjectName("actionRender_Blog")

        self.actionNewPost = QtGui.QAction(MainWindow)
        self.actionNewPost.setIcon(QtGui.QIcon(":/icons/icons/filenew.png"))
        self.actionNewPost.setObjectName("actionNewPost")

        self.actionConfigure = QtGui.QAction(MainWindow)
        self.actionConfigure.setIcon(QtGui.QIcon(":/icons/icons/configure.png"))
        self.actionConfigure.setObjectName("actionConfigure")

        self.actionImport_Advogato = QtGui.QAction(MainWindow)
        self.actionImport_Advogato.setObjectName("actionImport_Advogato")

        self.actionImport_PyDS = QtGui.QAction(MainWindow)
        self.actionImport_PyDS.setObjectName("actionImport_PyDS")
        self.menu_Post.addAction(self.actionEditPost)
        self.menu_File.addAction(self.actionNewPost)
        self.menu_File.addSeparator()
        self.menu_File.addSeparator()
        self.menuSettings.addAction(self.actionConfigure)
        self.menuBlog.addAction(self.actionRender_Blog)
        self.menuBlog.addSeparator()
        self.menuBlog.addAction(self.actionImport_Advogato)
        self.menuBlog.addAction(self.actionImport_PyDS)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Post.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuBlog.menuAction())
        self.toolBar.addAction(self.actionNewPost)
        self.toolBar.addAction(self.actionEditPost)
        self.toolBar.addAction(self.actionRender_Blog)
        self.toolBar.addAction(self.actionConfigure)
        self.label_2.setBuddy(self.link)

        self.retranslateUi(MainWindow)
        self.stack.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Link", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Post.setTitle(QtGui.QApplication.translate("MainWindow", "&Post", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSettings.setTitle(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menuBlog.setTitle(QtGui.QApplication.translate("MainWindow", "Blog", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditPost.setText(QtGui.QApplication.translate("MainWindow", "Edit Post", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRender_Blog.setText(QtGui.QApplication.translate("MainWindow", "Render Blog", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewPost.setText(QtGui.QApplication.translate("MainWindow", "New Post", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfigure.setText(QtGui.QApplication.translate("MainWindow", "Configure BartleBlog", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_Advogato.setText(QtGui.QApplication.translate("MainWindow", "Import Advogato", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_PyDS.setText(QtGui.QApplication.translate("MainWindow", "Import PyDS", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
