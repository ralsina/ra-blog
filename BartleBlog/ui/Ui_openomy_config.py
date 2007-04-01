# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/ra-blog/bartleblog/BartleBlog/ui/openomy_config.ui'
#
# Created: Sun Apr  1 13:08:47 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,539,380).size()).expandedTo(Form.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.textBrowser = QtGui.QTextBrowser(Form)
        self.textBrowser.setTabChangesFocus(True)
        self.textBrowser.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.vboxlayout.addWidget(self.textBrowser)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.status = QtGui.QLabel(Form)
        self.status.setObjectName("status")
        self.hboxlayout.addWidget(self.status)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)

        self.get = QtGui.QPushButton(Form)
        self.get.setObjectName("get")
        self.hboxlayout1.addWidget(self.get)

        self.forget = QtGui.QPushButton(Form)
        self.forget.setObjectName("forget")
        self.hboxlayout1.addWidget(self.forget)

        self.verify = QtGui.QPushButton(Form)
        self.verify.setObjectName("verify")
        self.hboxlayout1.addWidget(self.verify)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("Form", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:15pt; font-weight:600; text-decoration: underline;\">Important Information</span></p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To access your files in <a href=\"http://www.openomy.com\"><span style=\" text-decoration: underline; color:#0000ff;\">openomy.com</span></a>, BartleBlog needs to have an authorization token.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The way to get it is using your account information.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If you click on  \"Get Token\" you will be asked for your <a href=\"http://www.openomy.com\"><span style=\" text-decoration: underline; color:#0000ff;\">openomy.com</span></a> user name and password. BartleBlog will then obtain and save the token, and will not save the password information anywhere.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">However, the token will be saved in ~/.bartleblog.conf, and will allow BartleBlog to use your <a href=\"http://www.openomy.com\"><span style=\" text-decoration: underline; color:#0000ff;\">openomy.com</span></a> account. A malicious app could use that information to access your files.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can delete that information by clicking \"Forget Token\". In that case, you will be asked for your username and password whenever it is necessary and the token will <span style=\" font-weight:600;\">not</span> be saved.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Current Status:", None, QtGui.QApplication.UnicodeUTF8))
        self.status.setText(QtGui.QApplication.translate("Form", "Status goes here", None, QtGui.QApplication.UnicodeUTF8))
        self.get.setText(QtGui.QApplication.translate("Form", "Get Token", None, QtGui.QApplication.UnicodeUTF8))
        self.forget.setText(QtGui.QApplication.translate("Form", "Forget Token", None, QtGui.QApplication.UnicodeUTF8))
        self.verify.setText(QtGui.QApplication.translate("Form", "Verify Token", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
