# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/ra-blog/bartleblog/BartleBlog/ui/flickr.ui'
#
# Created: Tue Apr  3 12:20:44 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,713,572).size()).expandedTo(Dialog.minimumSizeHint()))

        self.hboxlayout = QtGui.QHBoxLayout(Dialog)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setObjectName("layoutWidget")
        self.hboxlayout.addWidget(self.layoutWidget)

        self.view = QtGui.QGraphicsView(Dialog)
        self.view.setObjectName("view")
        self.hboxlayout.addWidget(self.view)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.deleteBtn = QtGui.QPushButton(Dialog)
        self.deleteBtn.setObjectName("deleteBtn")
        self.vboxlayout.addWidget(self.deleteBtn)

        self.BlogBtn = QtGui.QPushButton(Dialog)
        self.BlogBtn.setObjectName("BlogBtn")
        self.vboxlayout.addWidget(self.BlogBtn)

        self.uploadBtn = QtGui.QPushButton(Dialog)
        self.uploadBtn.setObjectName("uploadBtn")
        self.vboxlayout.addWidget(self.uploadBtn)

        spacerItem = QtGui.QSpacerItem(20,331,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.closeBtn = QtGui.QPushButton(Dialog)
        self.closeBtn.setObjectName("closeBtn")
        self.vboxlayout.addWidget(self.closeBtn)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteBtn.setText(QtGui.QApplication.translate("Dialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.BlogBtn.setText(QtGui.QApplication.translate("Dialog", "Blog", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadBtn.setText(QtGui.QApplication.translate("Dialog", "Upload New Image", None, QtGui.QApplication.UnicodeUTF8))
        self.closeBtn.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
