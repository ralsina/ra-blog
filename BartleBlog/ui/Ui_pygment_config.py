# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/ra-blog/bartleblog/BartleBlog/ui/pygment_config.ui'
#
# Created: Thu Apr  5 14:15:23 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(Form.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.comboBox = QtGui.QComboBox(Form)
        self.comboBox.setObjectName("comboBox")
        self.hboxlayout.addWidget(self.comboBox)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.preview = QtGui.QTextBrowser(Form)
        self.preview.setObjectName("preview")
        self.vboxlayout.addWidget(self.preview)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)

        self.close = QtGui.QPushButton(Form)
        self.close.setObjectName("close")
        self.hboxlayout1.addWidget(self.close)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Color Scheme:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Preview:", None, QtGui.QApplication.UnicodeUTF8))
        self.preview.setHtml(QtGui.QApplication.translate("Form", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setText(QtGui.QApplication.translate("Form", "Close", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
