# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/bartleblog/trunk/BartleBlog/ui/blog_config.ui'
#
# Created: Fri Aug  3 19:57:28 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,400,637).size()).expandedTo(Form.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
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

        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.url = QtGui.QLineEdit(Form)
        self.url.setObjectName("url")
        self.gridlayout.addWidget(self.url,1,1,1,1)

        self.author = QtGui.QLineEdit(Form)
        self.author.setObjectName("author")
        self.gridlayout.addWidget(self.author,2,1,1,1)

        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.title = QtGui.QLineEdit(Form)
        self.title.setObjectName("title")
        self.gridlayout.addWidget(self.title,0,1,1,1)

        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridlayout.addWidget(self.label_6,4,0,1,1)

        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,2,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.folder = QtGui.QLineEdit(Form)
        self.folder.setObjectName("folder")
        self.hboxlayout.addWidget(self.folder)

        self.examine = QtGui.QPushButton(Form)
        self.examine.setObjectName("examine")
        self.hboxlayout.addWidget(self.examine)
        self.gridlayout.addLayout(self.hboxlayout,4,1,1,1)

        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,3,0,1,1)

        self.email = QtGui.QLineEdit(Form)
        self.email.setObjectName("email")
        self.gridlayout.addWidget(self.email,3,1,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.vboxlayout1.addWidget(self.label_5)

        self.description = QtGui.QTextEdit(Form)
        self.description.setObjectName("description")
        self.vboxlayout1.addWidget(self.description)
        self.vboxlayout.addLayout(self.vboxlayout1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)

        self.save = QtGui.QPushButton(Form)
        self.save.setObjectName("save")
        self.hboxlayout1.addWidget(self.save)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.label.setBuddy(self.title)
        self.label_2.setBuddy(self.url)
        self.label_6.setBuddy(self.folder)
        self.label_3.setBuddy(self.author)
        self.label_4.setBuddy(self.email)
        self.label_5.setBuddy(self.description)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.title,self.url)
        Form.setTabOrder(self.url,self.author)
        Form.setTabOrder(self.author,self.email)
        Form.setTabOrder(self.email,self.folder)
        Form.setTabOrder(self.folder,self.description)
        Form.setTabOrder(self.description,self.examine)
        Form.setTabOrder(self.examine,self.save)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Blog title:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Blog URL:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Form", "Blog Folder:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Author:", None, QtGui.QApplication.UnicodeUTF8))
        self.examine.setText(QtGui.QApplication.translate("Form", "Examine", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Author\'s email:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Blog\'s description:", None, QtGui.QApplication.UnicodeUTF8))
        self.save.setText(QtGui.QApplication.translate("Form", "Save", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
