# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/bartleblog/bartleblog/BartleBlog/ui/menu_config.ui'
#
# Created: Thu May 10 20:25:37 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,432,440).size()).expandedTo(Form.minimumSizeHint()))

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

        self.new = QtGui.QToolButton(Form)
        self.new.setIcon(QtGui.QIcon(":/icons/icons/filenew.svg"))
        self.new.setObjectName("new")
        self.hboxlayout1.addWidget(self.new)

        self.delete = QtGui.QToolButton(Form)
        self.delete.setEnabled(False)
        self.delete.setIcon(QtGui.QIcon(":/icons/icons/delete.svg"))
        self.delete.setObjectName("delete")
        self.hboxlayout1.addWidget(self.delete)

        self.preview = QtGui.QToolButton(Form)
        self.preview.setIcon(QtGui.QIcon(":/icons/icons/preview.svg"))
        self.preview.setObjectName("preview")
        self.hboxlayout1.addWidget(self.preview)

        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.hboxlayout1.addWidget(self.line)

        self.left = QtGui.QToolButton(Form)
        self.left.setEnabled(False)
        self.left.setIcon(QtGui.QIcon(":/icons/icons/1leftarrow.svg"))
        self.left.setObjectName("left")
        self.hboxlayout1.addWidget(self.left)

        self.right = QtGui.QToolButton(Form)
        self.right.setEnabled(False)
        self.right.setIcon(QtGui.QIcon(":/icons/icons/1rightarrow.svg"))
        self.right.setObjectName("right")
        self.hboxlayout1.addWidget(self.right)

        self.up = QtGui.QToolButton(Form)
        self.up.setEnabled(False)
        self.up.setIcon(QtGui.QIcon(":/icons/icons/1uparrow.svg"))
        self.up.setObjectName("up")
        self.hboxlayout1.addWidget(self.up)

        self.down = QtGui.QToolButton(Form)
        self.down.setEnabled(False)
        self.down.setIcon(QtGui.QIcon(":/icons/icons/1downarrow.svg"))
        self.down.setObjectName("down")
        self.hboxlayout1.addWidget(self.down)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.QLabel = QtGui.QLabel(Form)
        self.QLabel.setObjectName("QLabel")
        self.vboxlayout1.addWidget(self.QLabel)

        self.label = QtGui.QLineEdit(Form)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)

        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.vboxlayout1.addWidget(self.label_2)

        self.type = QtGui.QComboBox(Form)
        self.type.setObjectName("type")
        self.vboxlayout1.addWidget(self.type)

        self.data_type = QtGui.QLabel(Form)
        self.data_type.setObjectName("data_type")
        self.vboxlayout1.addWidget(self.data_type)

        self.extra_data = QtGui.QLineEdit(Form)
        self.extra_data.setEnabled(False)
        self.extra_data.setObjectName("extra_data")
        self.vboxlayout1.addWidget(self.extra_data)

        spacerItem = QtGui.QSpacerItem(122,41,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)

        self.save = QtGui.QPushButton(Form)
        self.save.setObjectName("save")
        self.vboxlayout1.addWidget(self.save)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.QLabel.setBuddy(self.QLabel)
        self.label_2.setBuddy(self.type)
        self.data_type.setBuddy(self.extra_data)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.QLabel,self.type)
        Form.setTabOrder(self.type,self.extra_data)
        Form.setTabOrder(self.extra_data,self.left)
        Form.setTabOrder(self.left,self.right)
        Form.setTabOrder(self.right,self.up)
        Form.setTabOrder(self.up,self.down)
        Form.setTabOrder(self.down,self.delete)
        Form.setTabOrder(self.delete,self.new)
        Form.setTabOrder(self.new,self.save)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.new.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.delete.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.preview.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.left.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.right.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.up.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.down.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.QLabel.setText(QtGui.QApplication.translate("Form", "Label:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.type.addItem(QtGui.QApplication.translate("Form", "Archives", None, QtGui.QApplication.UnicodeUTF8))
        self.type.addItem(QtGui.QApplication.translate("Form", "Label", None, QtGui.QApplication.UnicodeUTF8))
        self.type.addItem(QtGui.QApplication.translate("Form", "Link", None, QtGui.QApplication.UnicodeUTF8))
        self.type.addItem(QtGui.QApplication.translate("Form", "Story", None, QtGui.QApplication.UnicodeUTF8))
        self.type.addItem(QtGui.QApplication.translate("Form", "Tag", None, QtGui.QApplication.UnicodeUTF8))
        self.type.addItem(QtGui.QApplication.translate("Form", "Tag List", None, QtGui.QApplication.UnicodeUTF8))
        self.save.setText(QtGui.QApplication.translate("Form", "Save", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
