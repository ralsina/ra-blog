# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ralsina/Desktop/proyectos/bartleblog/trunk/BartleBlog/ui/choose_tags.ui'
#
# Created: Mon Mar  9 14:41:47 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.vboxlayout = QtGui.QVBoxLayout(Dialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        self.list = QtGui.QListWidget(Dialog)
        self.list.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.list.setObjectName("list")
        self.hboxlayout.addWidget(self.list)
        self.text = QtGui.QTextBrowser(Dialog)
        self.text.setObjectName("text")
        self.hboxlayout.addWidget(self.text)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")
        spacerItem = QtGui.QSpacerItem(131, 31, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setObjectName("okButton")
        self.hboxlayout1.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(Dialog)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout1.addWidget(self.cancelButton)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL("clicked()"), Dialog.accept)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("Dialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

