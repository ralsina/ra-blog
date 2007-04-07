# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/ra-blog/bartleblog/BartleBlog/ui/mainwindow.ui'
#
# Created: Sat Apr  7 12:57:11 2007
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

        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.tree = QtGui.QTreeView(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree.sizePolicy().hasHeightForWidth())
        self.tree.setSizePolicy(sizePolicy)
        self.tree.setSortingEnabled(False)
        self.tree.setAnimated(False)
        self.tree.setAllColumnsShowFocus(True)
        self.tree.setObjectName("tree")

        self.viewer = QtGui.QTextBrowser(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewer.sizePolicy().hasHeightForWidth())
        self.viewer.setSizePolicy(sizePolicy)

        font = QtGui.QFont(self.viewer.font())
        font.setFamily("Bitstream Vera Sans")
        self.viewer.setFont(font)
        self.viewer.setOpenExternalLinks(True)
        self.viewer.setObjectName("viewer")
        self.vboxlayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,686,31))
        self.menubar.setObjectName("menubar")

        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")

        self.menuImport = QtGui.QMenu(self.menu_File)
        self.menuImport.setObjectName("menuImport")

        self.menuBlog = QtGui.QMenu(self.menubar)
        self.menuBlog.setObjectName("menuBlog")

        self.menuRegenerate_HTML = QtGui.QMenu(self.menuBlog)
        self.menuRegenerate_HTML.setObjectName("menuRegenerate_HTML")

        self.menu_Post = QtGui.QMenu(self.menubar)
        self.menu_Post.setObjectName("menu_Post")
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

        self.actionRegenerateNeeded = QtGui.QAction(MainWindow)
        self.actionRegenerateNeeded.setObjectName("actionRegenerateNeeded")

        self.actionRegenerateAll = QtGui.QAction(MainWindow)
        self.actionRegenerateAll.setObjectName("actionRegenerateAll")

        self.actionDelete = QtGui.QAction(MainWindow)
        self.actionDelete.setIcon(QtGui.QIcon(":/icons/icons/fileclose.png"))
        self.actionDelete.setObjectName("actionDelete")
        self.menuSettings.addAction(self.actionConfigure)
        self.menuImport.addAction(self.actionImport_Advogato)
        self.menuImport.addAction(self.actionImport_PyDS)
        self.menu_File.addAction(self.actionNewPost)
        self.menu_File.addSeparator()
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.menuImport.menuAction())
        self.menuRegenerate_HTML.addAction(self.actionRegenerateNeeded)
        self.menuRegenerate_HTML.addAction(self.actionRegenerateAll)
        self.menuBlog.addAction(self.actionRender_Blog)
        self.menuBlog.addSeparator()
        self.menuBlog.addAction(self.menuRegenerate_HTML.menuAction())
        self.menu_Post.addAction(self.actionEditPost)
        self.menu_Post.addAction(self.actionDelete)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Post.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuBlog.menuAction())
        self.toolBar.addAction(self.actionNewPost)
        self.toolBar.addAction(self.actionEditPost)
        self.toolBar.addAction(self.actionRender_Blog)
        self.toolBar.addAction(self.actionConfigure)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSettings.setTitle(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuImport.setTitle(QtGui.QApplication.translate("MainWindow", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.menuBlog.setTitle(QtGui.QApplication.translate("MainWindow", "Blog", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRegenerate_HTML.setTitle(QtGui.QApplication.translate("MainWindow", "Regenerate HTML", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Post.setTitle(QtGui.QApplication.translate("MainWindow", "&Post", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditPost.setText(QtGui.QApplication.translate("MainWindow", "Edit Post", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRender_Blog.setText(QtGui.QApplication.translate("MainWindow", "Render Blog", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewPost.setText(QtGui.QApplication.translate("MainWindow", "New Post", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfigure.setText(QtGui.QApplication.translate("MainWindow", "Configure BartleBlog", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_Advogato.setText(QtGui.QApplication.translate("MainWindow", "Import Advogato", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_PyDS.setText(QtGui.QApplication.translate("MainWindow", "Import PyDS", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRegenerateNeeded.setText(QtGui.QApplication.translate("MainWindow", "Where necessary", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRegenerateAll.setText(QtGui.QApplication.translate("MainWindow", "Everywhere", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("MainWindow", "delete", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
