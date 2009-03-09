# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ralsina/Desktop/proyectos/bartleblog/trunk/BartleBlog/ui/flickr.ui'
#
# Created: Mon Mar  9 14:41:42 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(713, 572)
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
        spacerItem = QtGui.QSpacerItem(20, 331, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
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
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

