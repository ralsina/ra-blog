# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from BartleBlog.ui.Ui_translation_config import Ui_Form
import BartleBlog.backend.dbclasses as db
import BartleBlog.backend.config as config


class TranslationConfigWidget(QtGui.QWidget):
    def __init__(self, blog, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.curTranslation=None
        self.newName=None
        self.save=True

        # Set up the UI from designer
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        
        self.loadTranslations()

        QtCore.QObject.connect(self.ui.new,QtCore.SIGNAL('clicked()'),
            self.newTranslation)

        QtCore.QObject.connect(self.ui.delete,QtCore.SIGNAL('clicked()'),
            self.delTranslation)
            
        QtCore.QObject.connect(self.ui.list,QtCore.SIGNAL('itemClicked(QListWidgetItem *)'),
            self.loadTranslation)

        QtCore.QObject.connect(self.ui.code,QtCore.SIGNAL('textChanged(QString)'),
            self.saveTranslation)

        QtCore.QObject.connect(self.ui.name,QtCore.SIGNAL('textChanged(QString)'),
            self.saveTranslation)

        QtCore.QObject.connect(self.ui.defLangName,QtCore.SIGNAL('textChanged(QString)'),
            self.saveDefLang)
        QtCore.QObject.connect(self.ui.defLangCode,QtCore.SIGNAL('textChanged(QString)'),
            self.saveDefLang)
            
    def saveDefLang(self):
        config.setValue('blog', 'langcode', str(self.ui.defLangCode.text()))
        config.setValue('blog', 'langname', str(self.ui.defLangName.text()))

    def loadTranslation(self, item):
        name=str(item.text())
        print "Loading translation: ",name
        self.newName=None
        self.saveTranslation()
        sel=db.Translation.select(db.Translation.q.name==str(name))
        if sel.count()>0:
            self.curTranslation=db.Translation.select(db.Translation.q.name==str(name))[0]
        self.fillWidgets()
        
    def saveTranslation(self):
        if not self.curTranslation or not self.save:
            return
        self.curTranslation.name=str(self.ui.name.text())
        self.curTranslation.code=str(self.ui.code.text())
      
    def fillWidgets(self):
        print "CT: ", self.curTranslation
        self.save=False
        self.ui.name.setText('')
        self.ui.code.setText('')
        if self.curTranslation:
            if self.curTranslation.code:
                self.ui.code.setText(self.curTranslation.code)
            if self.curTranslation.name:
                self.ui.name.setText(self.curTranslation.name)
        self.save=True

    def delTranslation(self):
        print "CT ", self.curTranslation
        if not self.curTranslation:
            return
        res=QtGui.QMessageBox.question(self,'BartleBlog delete translation','Delete translation %s?'%self.curTranslation().name,
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if res == QtGui.QMessageBox.Yes:
            self.curTranslation().destroySelf()
            self.loadTranslations()

    def loadTranslations(self):
        self.ui.list.clear()
        for t in db.Translation.select(orderBy=db.Translation.q.name):
            self.ui.list.addItem(t.name)
            
        self.ui.defLangCode.setText(config.getValue('blog', 'langcode', 'en'))
        self.ui.defLangName.setText(config.getValue('blog', 'langname', 'English'))
                   
    def newTranslation(self):
        text,ok=QtGui.QInputDialog.getText(self,'BartleBlog - New Translation','Enter the name of the new translation')
        text=str(text)
        if ok:
            trans=db.Translation(name=text)
            self.loadTranslations()
