# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/bartleblog/trunk/BartleBlog/ui/translation_config.ui'
#
# Created: Tue Nov 20 12:15:22 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,537,546).size()).expandedTo(Form.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setObjectName("vboxlayout")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")

        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,0,0,1,1)

        self.defLangName = QtGui.QLineEdit(Form)
        self.defLangName.setObjectName("defLangName")
        self.gridlayout.addWidget(self.defLangName,0,1,1,1)

        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,1,0,1,1)

        self.defLangCode = QtGui.QLineEdit(Form)
        self.defLangCode.setObjectName("defLangCode")
        self.gridlayout.addWidget(self.defLangCode,1,1,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vboxlayout.addWidget(self.line)

        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.vboxlayout.addWidget(self.label_4)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.list = QtGui.QListWidget(Form)
        self.list.setObjectName("list")
        self.hboxlayout.addWidget(self.list)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.new = QtGui.QToolButton(Form)
        self.new.setIcon(QtGui.QIcon(":/icons/icons/filenew.svg"))
        self.new.setObjectName("new")
        self.hboxlayout1.addWidget(self.new)

        self.rename = QtGui.QToolButton(Form)
        self.rename.setIcon(QtGui.QIcon(":/icons/icons/edit.svg"))
        self.rename.setObjectName("rename")
        self.hboxlayout1.addWidget(self.rename)

        self.delete = QtGui.QToolButton(Form)
        self.delete.setIcon(QtGui.QIcon(":/icons/icons/delete.svg"))
        self.delete.setObjectName("delete")
        self.hboxlayout1.addWidget(self.delete)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)
        self.vboxlayout1.addLayout(self.hboxlayout1)

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName("gridlayout1")

        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.code = QtGui.QLineEdit(Form)
        self.code.setObjectName("code")
        self.gridlayout1.addWidget(self.code,0,1,1,1)

        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,1,0,1,1)

        self.name = QtGui.QLineEdit(Form)
        self.name.setObjectName("name")
        self.gridlayout1.addWidget(self.name,1,1,1,1)
        self.vboxlayout1.addLayout(self.gridlayout1)

        spacerItem1 = QtGui.QSpacerItem(20,61,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem1)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Default Language Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Default Language Code:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Translations", None, QtGui.QApplication.UnicodeUTF8))
        self.new.setToolTip(QtGui.QApplication.translate("Form", "New Translation", None, QtGui.QApplication.UnicodeUTF8))
        self.rename.setToolTip(QtGui.QApplication.translate("Form", "Rename Translation", None, QtGui.QApplication.UnicodeUTF8))
        self.rename.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.delete.setToolTip(QtGui.QApplication.translate("Form", "Delete Translation", None, QtGui.QApplication.UnicodeUTF8))
        self.delete.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Code:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Name:", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
