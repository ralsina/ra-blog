# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ralsina/Desktop/proyectos/bartleblog/trunk/BartleBlog/ui/mainwindow.ui'
#
# Created: Sat Aug  2 23:24:35 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(686,558)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0,65,686,469))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.tree = QtGui.QTreeView(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree.sizePolicy().hasHeightForWidth())
        self.tree.setSizePolicy(sizePolicy)
        self.tree.setSortingEnabled(False)
        self.tree.setAnimated(False)
        self.tree.setAllColumnsShowFocus(True)
        self.tree.setObjectName("tree")
        self.viewer = PBrowser(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored,QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewer.sizePolicy().hasHeightForWidth())
        self.viewer.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.viewer.setFont(font)
        self.viewer.setOpenExternalLinks(True)
        self.viewer.setObjectName("viewer")
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,686,27))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menu_Post = QtGui.QMenu(self.menubar)
        self.menu_Post.setObjectName("menu_Post")
        self.menuBlog = QtGui.QMenu(self.menubar)
        self.menuBlog.setObjectName("menuBlog")
        self.menuRegenerate_HTML = QtGui.QMenu(self.menuBlog)
        self.menuRegenerate_HTML.setObjectName("menuRegenerate_HTML")
        self.menuRender_Pages = QtGui.QMenu(self.menuBlog)
        self.menuRender_Pages.setObjectName("menuRender_Pages")
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setGeometry(QtCore.QRect(0,0,200,166))
        self.menu_File.setObjectName("menu_File")
        self.menuImport = QtGui.QMenu(self.menu_File)
        self.menuImport.setObjectName("menuImport")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setGeometry(QtCore.QRect(0,534,686,24))
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setGeometry(QtCore.QRect(0,27,686,38))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setIconSize(QtCore.QSize(24,24))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea,self.toolBar)
        self.actionEditPost = QtGui.QAction(MainWindow)
        self.actionEditPost.setCheckable(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/edit.svg"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.actionEditPost.setIcon(icon)
        self.actionEditPost.setObjectName("actionEditPost")
        self.actionRender_Blog = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/webexport.svg"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.actionRender_Blog.setIcon(icon)
        self.actionRender_Blog.setObjectName("actionRender_Blog")
        self.actionNewPost = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/filenew.svg"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.actionNewPost.setIcon(icon)
        self.actionNewPost.setObjectName("actionNewPost")
        self.actionConfigure = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/configure.svg"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.actionConfigure.setIcon(icon)
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/delete.svg"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon)
        self.actionDelete.setObjectName("actionDelete")
        self.actionRender_Full_Blog = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/webexport.svg"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.actionRender_Full_Blog.setIcon(icon)
        self.actionRender_Full_Blog.setObjectName("actionRender_Full_Blog")
        self.actionAbout_BartleBlog = QtGui.QAction(MainWindow)
        self.actionAbout_BartleBlog.setObjectName("actionAbout_BartleBlog")
        self.actionNew_Story = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/filenew.svg"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.actionNew_Story.setIcon(icon)
        self.actionNew_Story.setObjectName("actionNew_Story")
        self.actionQuit = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/exit.svg"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon)
        self.actionQuit.setObjectName("actionQuit")
        self.actionBartleBlog_Help = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/help.svg"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.actionBartleBlog_Help.setIcon(icon)
        self.actionBartleBlog_Help.setObjectName("actionBartleBlog_Help")
        self.menuSettings.addAction(self.actionConfigure)
        self.menu_Post.addAction(self.actionEditPost)
        self.menu_Post.addAction(self.actionDelete)
        self.menuRegenerate_HTML.addAction(self.actionRegenerateNeeded)
        self.menuRegenerate_HTML.addAction(self.actionRegenerateAll)
        self.menuRender_Pages.addAction(self.actionRender_Blog)
        self.menuRender_Pages.addAction(self.actionRender_Full_Blog)
        self.menuBlog.addSeparator()
        self.menuBlog.addAction(self.menuRender_Pages.menuAction())
        self.menuBlog.addAction(self.menuRegenerate_HTML.menuAction())
        self.menuImport.addAction(self.actionImport_Advogato)
        self.menuImport.addAction(self.actionImport_PyDS)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionNewPost)
        self.menu_File.addAction(self.actionNew_Story)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.menuImport.menuAction())
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionBartleBlog_Help)
        self.menuHelp.addAction(self.actionAbout_BartleBlog)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Post.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuBlog.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionNewPost)
        self.toolBar.addAction(self.actionEditPost)
        self.toolBar.addAction(self.actionRender_Blog)
        self.toolBar.addAction(self.actionConfigure)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSettings.setTitle(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Post.setTitle(QtGui.QApplication.translate("MainWindow", "&Post", None, QtGui.QApplication.UnicodeUTF8))
        self.menuBlog.setTitle(QtGui.QApplication.translate("MainWindow", "Blog", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRegenerate_HTML.setTitle(QtGui.QApplication.translate("MainWindow", "Regenerate HTML", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRender_Pages.setTitle(QtGui.QApplication.translate("MainWindow", "Render Pages", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuImport.setTitle(QtGui.QApplication.translate("MainWindow", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditPost.setText(QtGui.QApplication.translate("MainWindow", "Edit Post", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRender_Blog.setText(QtGui.QApplication.translate("MainWindow", "Render Blog", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewPost.setText(QtGui.QApplication.translate("MainWindow", "New Post", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfigure.setText(QtGui.QApplication.translate("MainWindow", "Configure BartleBlog", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_Advogato.setText(QtGui.QApplication.translate("MainWindow", "Import Advogato", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_PyDS.setText(QtGui.QApplication.translate("MainWindow", "Import PyDS", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRegenerateNeeded.setText(QtGui.QApplication.translate("MainWindow", "Where necessary", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRegenerateAll.setText(QtGui.QApplication.translate("MainWindow", "Everywhere", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("MainWindow", "delete", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRender_Full_Blog.setText(QtGui.QApplication.translate("MainWindow", "Render Full Blog", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_BartleBlog.setText(QtGui.QApplication.translate("MainWindow", "About BartleBlog", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_Story.setText(QtGui.QApplication.translate("MainWindow", "New Story", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBartleBlog_Help.setText(QtGui.QApplication.translate("MainWindow", "BartleBlog Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBartleBlog_Help.setShortcut(QtGui.QApplication.translate("MainWindow", "F1", None, QtGui.QApplication.UnicodeUTF8))

from pbrowser import PBrowser
import icons_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

