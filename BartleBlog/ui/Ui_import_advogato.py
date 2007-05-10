# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/bartleblog/bartleblog/BartleBlog/ui/import_advogato.ui'
#
# Created: Thu May 10 14:04:33 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,455,366).size()).expandedTo(Dialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Dialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.textBrowser = QtGui.QTextBrowser(Dialog)
        self.textBrowser.setObjectName("textBrowser")
        self.vboxlayout.addWidget(self.textBrowser)

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.prefix = QtGui.QLineEdit(Dialog)
        self.prefix.setMaxLength(8)
        self.prefix.setObjectName("prefix")
        self.gridlayout.addWidget(self.prefix,2,1,1,1)

        self.user = QtGui.QLineEdit(Dialog)
        self.user.setObjectName("user")
        self.gridlayout.addWidget(self.user,0,1,1,2)

        self.sameprefix = QtGui.QLabel(Dialog)
        self.sameprefix.setObjectName("sameprefix")
        self.gridlayout.addWidget(self.sameprefix,2,2,1,1)

        self.password = QtGui.QLineEdit(Dialog)
        self.password.setObjectName("password")
        self.gridlayout.addWidget(self.password,1,1,1,2)

        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,2,0,1,1)

        self.overwrite = QtGui.QCheckBox(Dialog)
        self.overwrite.setObjectName("overwrite")
        self.gridlayout.addWidget(self.overwrite,3,0,1,3)

        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,0,0,1,1)

        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,1,0,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.cancel = QtGui.QPushButton(Dialog)
        self.cancel.setObjectName("cancel")
        self.hboxlayout.addWidget(self.cancel)

        self.do_import = QtGui.QPushButton(Dialog)
        self.do_import.setObjectName("do_import")
        self.hboxlayout.addWidget(self.do_import)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">BartleBlog can import the posts from an Advogato account.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">To do that, you need to enter your username and password (which will not be saved anywhere) and a prefix for PostIDs. For example, if the prefix is ADV, the posts will be ADV1, ADV2, etc.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This is only important if you intend to import more than one advogato account, since PostIDs need to be unique.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.sameprefix.setText(QtGui.QApplication.translate("Dialog", "N posts with that prefix", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Post ID Prefix:", None, QtGui.QApplication.UnicodeUTF8))
        self.overwrite.setText(QtGui.QApplication.translate("Dialog", "Overwrite existing posts with same Post ID", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "User:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.do_import.setText(QtGui.QApplication.translate("Dialog", "Import", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
