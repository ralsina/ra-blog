# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/bartleblog/trunk/BartleBlog/ui/translation_config.ui'
#
# Created: Mon Nov 19 18:32:17 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,537,431).size()).expandedTo(Form.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.new = QtGui.QToolButton(Form)
        self.new.setIcon(QtGui.QIcon(":/icons/icons/filenew.svg"))
        self.new.setObjectName("new")
        self.hboxlayout.addWidget(self.new)

        self.rename = QtGui.QToolButton(Form)
        self.rename.setIcon(QtGui.QIcon(":/icons/icons/edit.svg"))
        self.rename.setObjectName("rename")
        self.hboxlayout.addWidget(self.rename)

        self.delete = QtGui.QToolButton(Form)
        self.delete.setIcon(QtGui.QIcon(":/icons/icons/delete.svg"))
        self.delete.setObjectName("delete")
        self.hboxlayout.addWidget(self.delete)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.list = QtGui.QListWidget(Form)
        self.list.setObjectName("list")
        self.vboxlayout.addWidget(self.list)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.new.setToolTip(QtGui.QApplication.translate("Form", "New Translation", None, QtGui.QApplication.UnicodeUTF8))
        self.rename.setToolTip(QtGui.QApplication.translate("Form", "Rename Translation", None, QtGui.QApplication.UnicodeUTF8))
        self.rename.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.delete.setToolTip(QtGui.QApplication.translate("Form", "Delete Translation", None, QtGui.QApplication.UnicodeUTF8))
        self.delete.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
