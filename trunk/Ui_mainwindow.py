# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/ra-blog/svn/mainwindow.ui'
#
# Created: Fri Mar 23 17:40:20 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,755,645).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.link = QtGui.QLineEdit(self.centralwidget)
        self.link.setObjectName("link")
        self.gridlayout.addWidget(self.link,1,1,1,1)

        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.title = QtGui.QLineEdit(self.centralwidget)
        self.title.setObjectName("title")
        self.gridlayout.addWidget(self.title,0,1,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.tree = QtGui.QTreeView(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree.sizePolicy().hasHeightForWidth())
        self.tree.setSizePolicy(sizePolicy)
        self.tree.setSortingEnabled(True)
        self.tree.setAnimated(False)
        self.tree.setAllColumnsShowFocus(True)
        self.tree.setObjectName("tree")
        self.hboxlayout.addWidget(self.tree)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.stack = QtGui.QStackedWidget(self.centralwidget)
        self.stack.setObjectName("stack")

        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.page_2)
        self.hboxlayout1.setMargin(9)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.viewer = QtGui.QTextBrowser(self.page_2)
        self.viewer.setObjectName("viewer")
        self.hboxlayout1.addWidget(self.viewer)
        self.stack.addWidget(self.page_2)

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.hboxlayout2 = QtGui.QHBoxLayout(self.page)
        self.hboxlayout2.setMargin(9)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.editor = QtGui.QTextEdit(self.page)
        self.editor.setObjectName("editor")
        self.hboxlayout2.addWidget(self.editor)
        self.stack.addWidget(self.page)
        self.vboxlayout1.addWidget(self.stack)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout3.addWidget(self.pushButton)

        self.categories = QtGui.QLabel(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categories.sizePolicy().hasHeightForWidth())
        self.categories.setSizePolicy(sizePolicy)
        self.categories.setObjectName("categories")
        self.hboxlayout3.addWidget(self.categories)
        self.vboxlayout1.addLayout(self.hboxlayout3)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.vboxlayout.addLayout(self.hboxlayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,755,32))
        self.menubar.setObjectName("menubar")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")

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

        self.actionEdit_Item = QtGui.QAction(MainWindow)
        self.actionEdit_Item.setCheckable(True)
        self.actionEdit_Item.setIcon(QtGui.QIcon("../../../../../../../../opt/kde/share/icons/crystalsvg/32x32/actions/edit.png"))
        self.actionEdit_Item.setObjectName("actionEdit_Item")

        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")

        self.actionRst = QtGui.QAction(MainWindow)
        self.actionRst.setCheckable(True)
        self.actionRst.setChecked(True)
        self.actionRst.setIcon(QtGui.QIcon("../../../../../../../../opt/kde/share/icons/crystalsvg/32x32/actions/fonts.png"))
        self.actionRst.setObjectName("actionRst")
        self.menu_File.addSeparator()
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_Post.addAction(self.actionEdit_Item)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Post.menuAction())
        self.toolBar.addAction(self.actionEdit_Item)
        self.toolBar.addAction(self.actionRst)
        self.label_2.setBuddy(self.link)
        self.categories.setBuddy(self.pushButton)

        self.retranslateUi(MainWindow)
        self.stack.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Link", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Categories", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Post.setTitle(QtGui.QApplication.translate("MainWindow", "&Post", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_Item.setText(QtGui.QApplication.translate("MainWindow", "Edit Post", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRst.setText(QtGui.QApplication.translate("MainWindow", "Rst", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
