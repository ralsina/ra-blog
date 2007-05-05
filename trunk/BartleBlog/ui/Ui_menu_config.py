# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/bartleblog/bartleblog/BartleBlog/ui/menu_config.ui'
#
# Created: Sat May  5 13:05:38 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(Form.minimumSizeHint()))

        self.hboxlayout = QtGui.QHBoxLayout(Form)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tree = QtGui.QTreeWidget(Form)
        self.tree.setObjectName("tree")
        self.vboxlayout.addWidget(self.tree)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.left = QtGui.QToolButton(Form)
        self.left.setObjectName("left")
        self.hboxlayout1.addWidget(self.left)

        self.right = QtGui.QToolButton(Form)
        self.right.setObjectName("right")
        self.hboxlayout1.addWidget(self.right)

        self.up = QtGui.QToolButton(Form)
        self.up.setObjectName("up")
        self.hboxlayout1.addWidget(self.up)

        self.down = QtGui.QToolButton(Form)
        self.down.setObjectName("down")
        self.hboxlayout1.addWidget(self.down)

        self.delete = QtGui.QToolButton(Form)
        self.delete.setObjectName("delete")
        self.hboxlayout1.addWidget(self.delete)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.type = QtGui.QComboBox(Form)
        self.type.setObjectName("type")
        self.vboxlayout1.addWidget(self.type)

        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)

        self.label1 = QtGui.QLineEdit(Form)
        self.label1.setObjectName("label1")
        self.vboxlayout1.addWidget(self.label1)

        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.vboxlayout1.addWidget(self.label_2)

        self.special = QtGui.QLineEdit(Form)
        self.special.setObjectName("special")
        self.vboxlayout1.addWidget(self.special)

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)
        self.hboxlayout.addLayout(self.vboxlayout1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.left.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.right.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.up.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.down.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.delete.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Label:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Special", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
