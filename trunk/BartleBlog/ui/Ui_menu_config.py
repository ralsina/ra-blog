# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ralsina/Desktop/proyectos/bartleblog/trunk/BartleBlog/ui/menu_config.ui'
#
# Created: Mon Mar  9 14:41:47 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(432, 440)
        self.hboxlayout = QtGui.QHBoxLayout(Form)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.tree = QtGui.QTreeWidget(Form)
        self.tree.setColumnCount(1)
        self.tree.setObjectName("tree")
        self.vboxlayout.addWidget(self.tree)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.new = QtGui.QToolButton(Form)
        icon = QtGui.QIcon()
        icon.addFile(":/icons/icons/filenew.svg")
        self.new.setIcon(icon)
        self.new.setObjectName("new")
        self.hboxlayout1.addWidget(self.new)
        self.delete = QtGui.QToolButton(Form)
        self.delete.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addFile(":/icons/icons/delete.svg")
        self.delete.setIcon(icon1)
        self.delete.setObjectName("delete")
        self.hboxlayout1.addWidget(self.delete)
        self.preview = QtGui.QToolButton(Form)
        icon2 = QtGui.QIcon()
        icon2.addFile(":/icons/icons/preview.svg")
        self.preview.setIcon(icon2)
        self.preview.setObjectName("preview")
        self.hboxlayout1.addWidget(self.preview)
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.hboxlayout1.addWidget(self.line)
        self.left = QtGui.QToolButton(Form)
        self.left.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addFile(":/icons/icons/1leftarrow.svg")
        self.left.setIcon(icon3)
        self.left.setObjectName("left")
        self.hboxlayout1.addWidget(self.left)
        self.right = QtGui.QToolButton(Form)
        self.right.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addFile(":/icons/icons/1rightarrow.svg")
        self.right.setIcon(icon4)
        self.right.setObjectName("right")
        self.hboxlayout1.addWidget(self.right)
        self.up = QtGui.QToolButton(Form)
        self.up.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addFile(":/icons/icons/1uparrow.svg")
        self.up.setIcon(icon5)
        self.up.setObjectName("up")
        self.hboxlayout1.addWidget(self.up)
        self.down = QtGui.QToolButton(Form)
        self.down.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addFile(":/icons/icons/1downarrow.svg")
        self.down.setIcon(icon6)
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
        self.label.setEnabled(False)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.vboxlayout1.addWidget(self.label_2)
        self.type = QtGui.QComboBox(Form)
        self.type.setEnabled(False)
        self.type.setObjectName("type")
        self.type.addItem(QtCore.QString())
        self.type.addItem(QtCore.QString())
        self.type.addItem(QtCore.QString())
        self.type.addItem(QtCore.QString())
        self.type.addItem(QtCore.QString())
        self.type.addItem(QtCore.QString())
        self.type.addItem(QtCore.QString())
        self.vboxlayout1.addWidget(self.type)
        self.data_type = QtGui.QLabel(Form)
        self.data_type.setObjectName("data_type")
        self.vboxlayout1.addWidget(self.data_type)
        self.extra_data = QtGui.QLineEdit(Form)
        self.extra_data.setEnabled(True)
        self.extra_data.setObjectName("extra_data")
        self.vboxlayout1.addWidget(self.extra_data)
        spacerItem = QtGui.QSpacerItem(122, 41, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
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
        Form.setTabOrder(self.QLabel, self.type)
        Form.setTabOrder(self.type, self.extra_data)
        Form.setTabOrder(self.extra_data, self.left)
        Form.setTabOrder(self.left, self.right)
        Form.setTabOrder(self.right, self.up)
        Form.setTabOrder(self.up, self.down)
        Form.setTabOrder(self.down, self.delete)
        Form.setTabOrder(self.delete, self.new)
        Form.setTabOrder(self.new, self.save)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(0, QtGui.QApplication.translate("Form", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.new.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.delete.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.preview.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.left.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.right.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.up.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.down.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.QLabel.setText(QtGui.QApplication.translate("Form", "Label:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.type.setItemText(0, QtGui.QApplication.translate("Form", "Archives", None, QtGui.QApplication.UnicodeUTF8))
        self.type.setItemText(1, QtGui.QApplication.translate("Form", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.type.setItemText(2, QtGui.QApplication.translate("Form", "Label", None, QtGui.QApplication.UnicodeUTF8))
        self.type.setItemText(3, QtGui.QApplication.translate("Form", "Link", None, QtGui.QApplication.UnicodeUTF8))
        self.type.setItemText(4, QtGui.QApplication.translate("Form", "Story", None, QtGui.QApplication.UnicodeUTF8))
        self.type.setItemText(5, QtGui.QApplication.translate("Form", "Tag", None, QtGui.QApplication.UnicodeUTF8))
        self.type.setItemText(6, QtGui.QApplication.translate("Form", "Tag List", None, QtGui.QApplication.UnicodeUTF8))
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

