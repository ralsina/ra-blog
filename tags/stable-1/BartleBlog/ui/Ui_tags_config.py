# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/bartleblog/trunk/BartleBlog/ui/tags_config.ui'
#
# Created: Fri Aug  3 19:57:25 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,572,510).size()).expandedTo(Form.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)

        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.list = QtGui.QComboBox(Form)
        self.list.setEditable(False)
        self.list.setObjectName("list")
        self.hboxlayout.addWidget(self.list)

        self.new = QtGui.QToolButton(Form)
        self.new.setIcon(QtGui.QIcon(":/icons/icons/filenew.svg"))
        self.new.setObjectName("new")
        self.hboxlayout.addWidget(self.new)

        self.delete = QtGui.QToolButton(Form)
        self.delete.setIcon(QtGui.QIcon(":/icons/icons/delete.svg"))
        self.delete.setObjectName("delete")
        self.hboxlayout.addWidget(self.delete)

        self.rename = QtGui.QToolButton(Form)
        self.rename.setIcon(QtGui.QIcon(":/icons/icons/edit.svg"))
        self.rename.setObjectName("rename")
        self.hboxlayout.addWidget(self.rename)

        self.autotag = QtGui.QToolButton(Form)
        self.autotag.setIcon(QtGui.QIcon(":/icons/icons/find.svg"))
        self.autotag.setObjectName("autotag")
        self.hboxlayout.addWidget(self.autotag)

        spacerItem = QtGui.QSpacerItem(241,25,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.gridlayout.addLayout(self.hboxlayout,0,1,1,1)

        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,2,0,1,1)

        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,1,0,1,1)

        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.title = QtGui.QLineEdit(Form)
        self.title.setObjectName("title")
        self.gridlayout.addWidget(self.title,1,1,1,1)

        self.magicWords = QtGui.QLineEdit(Form)
        self.magicWords.setObjectName("magicWords")
        self.gridlayout.addWidget(self.magicWords,2,1,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.vboxlayout.addWidget(self.label_3)

        self.description = QtGui.QTextEdit(Form)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy)
        self.description.setObjectName("description")
        self.vboxlayout.addWidget(self.description)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.new.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.delete.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.rename.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.autotag.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Magic Words:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Title:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Tags:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Description:", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())