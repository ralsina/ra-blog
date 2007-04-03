# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/ra-blog/bartleblog/BartleBlog/ui/rsteditor.ui'
#
# Created: Tue Apr  3 20:49:38 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,800,600).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.centralWidget)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.tags = QtGui.QLineEdit(self.centralWidget)
        self.tags.setObjectName("tags")
        self.gridlayout.addWidget(self.tags,2,1,1,1)

        self.format = QtGui.QComboBox(self.centralWidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.format.sizePolicy().hasHeightForWidth())
        self.format.setSizePolicy(sizePolicy)
        self.format.setObjectName("format")
        self.gridlayout.addWidget(self.format,2,3,1,1)

        self.title = QtGui.QLineEdit(self.centralWidget)
        self.title.setObjectName("title")
        self.gridlayout.addWidget(self.title,0,1,1,3)

        self.label_3 = QtGui.QLabel(self.centralWidget)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,2,2,1,1)

        self.link = QtGui.QLineEdit(self.centralWidget)
        self.link.setObjectName("link")
        self.gridlayout.addWidget(self.link,1,1,1,2)

        self.pushButton = QtGui.QPushButton(self.centralWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,1,3,1,1)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)

        self.label_4 = QtGui.QLabel(self.centralWidget)
        self.label_4.setObjectName("label_4")
        self.vboxlayout1.addWidget(self.label_4)

        self.label_2 = QtGui.QLabel(self.centralWidget)
        self.label_2.setObjectName("label_2")
        self.vboxlayout1.addWidget(self.label_2)
        self.gridlayout.addLayout(self.vboxlayout1,0,0,3,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.editor = QtGui.QTextEdit(self.centralWidget)
        self.editor.setAcceptRichText(False)
        self.editor.setObjectName("editor")
        self.vboxlayout.addWidget(self.editor)
        MainWindow.setCentralWidget(self.centralWidget)

        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0,0,800,31))
        self.menuBar.setObjectName("menuBar")

        self.menuPost = QtGui.QMenu(self.menuBar)
        self.menuPost.setObjectName("menuPost")

        self.menuEdit = QtGui.QMenu(self.menuBar)
        self.menuEdit.setObjectName("menuEdit")

        self.menuInsert = QtGui.QMenu(self.menuEdit)
        self.menuInsert.setObjectName("menuInsert")
        MainWindow.setMenuBar(self.menuBar)

        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(self.toolBar)

        self.actionPreview = QtGui.QAction(MainWindow)
        self.actionPreview.setIcon(QtGui.QIcon(":/icons/icons/xeyes.png"))
        self.actionPreview.setObjectName("actionPreview")

        self.actionCut = QtGui.QAction(MainWindow)
        self.actionCut.setIcon(QtGui.QIcon(":/icons/icons/editcut.png"))
        self.actionCut.setObjectName("actionCut")

        self.actionCopy = QtGui.QAction(MainWindow)
        self.actionCopy.setIcon(QtGui.QIcon(":/icons/icons/editcopy.png"))
        self.actionCopy.setObjectName("actionCopy")

        self.actionPaste = QtGui.QAction(MainWindow)
        self.actionPaste.setIcon(QtGui.QIcon(":/icons/icons/editpaste.png"))
        self.actionPaste.setObjectName("actionPaste")

        self.actionUndo = QtGui.QAction(MainWindow)
        self.actionUndo.setIcon(QtGui.QIcon(":/icons/icons/undo.png"))
        self.actionUndo.setObjectName("actionUndo")

        self.actionRedo = QtGui.QAction(MainWindow)
        self.actionRedo.setIcon(QtGui.QIcon(":/icons/icons/redo.png"))
        self.actionRedo.setObjectName("actionRedo")

        self.actionDelete = QtGui.QAction(MainWindow)
        self.actionDelete.setObjectName("actionDelete")

        self.actionSelect_All = QtGui.QAction(MainWindow)
        self.actionSelect_All.setObjectName("actionSelect_All")

        self.actionFlickr_Image = QtGui.QAction(MainWindow)
        self.actionFlickr_Image.setIcon(QtGui.QIcon(":/icons/icons/camera.png"))
        self.actionFlickr_Image.setObjectName("actionFlickr_Image")

        self.actionOpenomy_File = QtGui.QAction(MainWindow)
        self.actionOpenomy_File.setIcon(QtGui.QIcon(":/icons/icons/blockdevice.png"))
        self.actionOpenomy_File.setObjectName("actionOpenomy_File")

        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setIcon(QtGui.QIcon(":/icons/icons/filesave.png"))
        self.actionSave.setObjectName("actionSave")

        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setIcon(QtGui.QIcon(":/icons/icons/fileclose.png"))
        self.actionClose.setObjectName("actionClose")

        self.actionOpenomyTag = QtGui.QAction(MainWindow)
        self.actionOpenomyTag.setIcon(QtGui.QIcon(":/icons/icons/blockdevice.png"))
        self.actionOpenomyTag.setObjectName("actionOpenomyTag")
        self.menuPost.addAction(self.actionSave)
        self.menuPost.addAction(self.actionPreview)
        self.menuPost.addSeparator()
        self.menuPost.addAction(self.actionClose)
        self.menuInsert.addAction(self.actionFlickr_Image)
        self.menuInsert.addAction(self.actionOpenomy_File)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addAction(self.actionSelect_All)
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.menuInsert.menuAction())
        self.menuBar.addAction(self.menuPost.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionPreview)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCut)
        self.toolBar.addAction(self.actionCopy)
        self.toolBar.addAction(self.actionPaste)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionUndo)
        self.toolBar.addAction(self.actionRedo)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionFlickr_Image)
        self.toolBar.addAction(self.actionOpenomy_File)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.title,self.link)
        MainWindow.setTabOrder(self.link,self.tags)
        MainWindow.setTabOrder(self.tags,self.editor)
        MainWindow.setTabOrder(self.editor,self.format)
        MainWindow.setTabOrder(self.format,self.pushButton)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.format.addItem(QtGui.QApplication.translate("MainWindow", "Restructured Text", None, QtGui.QApplication.UnicodeUTF8))
        self.format.addItem(QtGui.QApplication.translate("MainWindow", "HTML", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Format:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Make &Tiny", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Title:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Link:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Tags:", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPost.setTitle(QtGui.QApplication.translate("MainWindow", "Post", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuInsert.setTitle(QtGui.QApplication.translate("MainWindow", "Insert", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreview.setText(QtGui.QApplication.translate("MainWindow", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("MainWindow", "Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("MainWindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUndo.setText(QtGui.QApplication.translate("MainWindow", "Undo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRedo.setText(QtGui.QApplication.translate("MainWindow", "Redo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelect_All.setText(QtGui.QApplication.translate("MainWindow", "Select All", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFlickr_Image.setText(QtGui.QApplication.translate("MainWindow", "Flickr Image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenomy_File.setText(QtGui.QApplication.translate("MainWindow", "Openomy File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenomyTag.setText(QtGui.QApplication.translate("MainWindow", "Openomy Tag", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
