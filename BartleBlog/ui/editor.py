# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import time

from BartleBlog.ui.Ui_rsteditor import Ui_MainWindow
from BartleBlog.ui.choose_tags import TagsDialog
import BartleBlog.backend.dbclasses as db
from rsthighlight import rstHighlighter
import datetime

class EditorWindow(QtGui.QMainWindow):
    def __init__(self,post=None, previews=True, lang=None):
        QtGui.QMainWindow.__init__(self)

        # Set up the UI from designer
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.langs=QtGui.QComboBox(self)
        self.langs.setEnabled(False)
        self.langs.addItem("Default")
        for lang in db.Translation.select():
            self.langs.addItem(lang.name)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addWidget(self.langs)

        self.trPost=None
        self.setPost(post)

        self.setLang(lang)
        QtCore.QObject.connect(self.langs,
            QtCore.SIGNAL("activated (QString)"),
            self.setLang)

        QtCore.QObject.connect(self.ui.actionSave,
            QtCore.SIGNAL("triggered()"),
            self.savePost)

        QtCore.QObject.connect(self.ui.actionClose,
            QtCore.SIGNAL("triggered()"),
            self.closeWindow)

        if previews:
            QtCore.QObject.connect(self.ui.actionPreview,
                QtCore.SIGNAL("triggered()"),
                self.preview)
        else:
            self.ui.actionPreview.setEnabled(False)

        QtCore.QObject.connect(self.ui.guess,
            QtCore.SIGNAL("clicked()"),
            self.guessTags)

        QtCore.QObject.connect(self.ui.tags,
            QtCore.SIGNAL("clicked()"),
            self.chooseTags)
            
        #self.hl=rstHighlighter(self.ui.editor.document())
        self.previewPost=None

    def setLang(self, lang):
        if not lang: # None is "default language"
            return
        
        lang=unicode(lang)
        if lang=="Default":
            self.lang=None
            self.trPost=None
        # Find the posts translation for this language
        if self.post:
            self.lang=lang
            self.trPost=db.translationByLangNamePost(lang, self.post)
            self.setPost(self.post)
        # There is no post set, so there can't be a translation
        # This shouldn't happen

    def chooseTags(self):
        self.d=TagsDialog(self,self.ui.tags.text())
        r=self.d.exec_()

        if r:
            self.ui.tags.setText(self.d.currentCategories())
        del self.d

    def guessTags(self):
        self.ui.tags.setText(','.join(db.guessCategories(unicode(self.ui.editor.toPlainText())+unicode(self.ui.title.text()))))

    def closeWindow(self):
        self.close()

    def setPost(self,post):
        self.post=post
        if not post:
            return

        print "TR:", post.translations()

        self.langs.setEnabled(True)

        # Maybe this is a translation
        if self.trPost and self.lang:
            self.ui.title.setText(self.trPost.title)
            self.ui.editor.setPlainText(self.trPost.text)        
        else: # Maybe not
            self.ui.title.setText(post.title)
            self.ui.editor.setPlainText(post.text)
            
        self.ui.link.setText(post.link)
        self.ui.tags.setText(','.join( [c.name for c in post.categories]))
        self.ui.actionRST.setChecked(post.structured)

    def savePost(self):
        # FIXME: make the TZ configurable
        if not self.post:
            print "Saving new post"
            self.post=db.Post( postID="BB%s"%str(time.time()),
                            title=unicode(self.ui.title.text()),
                            link=unicode(self.ui.link.text()),
                            text=unicode(self.ui.editor.toPlainText()), 
                            structured=self.ui.actionRST.isChecked(),
                            pubDate=datetime.datetime.utcnow(),
                            modDate=datetime.datetime.utcnow())
            # Silly hack to have PostID be unique but not ugly
            self.post.postID='BB'+str(self.post.id)
        else:
            if self.trPost and self.lang: #Translation
                print "Saving translated post"
                self.trPost.title=unicode(self.ui.title.text())
                self.trPost.text=unicode(self.ui.editor.toPlainText())
                self.trPost.structured=self.ui.actionRST.isChecked()
                self.trPost.render()
            else: # Default lang
                print "Saving untranslated post"
                self.post.title=unicode(self.ui.title.text())
                self.post.text=unicode(self.ui.editor.toPlainText())
                self.post.structured=self.ui.actionRST.isChecked()
                self.post.render(),
                self.post.modDate=datetime.datetime.utcnow()
            self.post.link=str(self.ui.link.text())
        t=unicode(self.ui.tags.text())
        if t:
            cats=[ db.Category.select(db.Category.q.name==c)[0] for c in \
                t.split(',') ]
            self.post.setCategories(cats)
        self.post.render()
        self.post.setDirtyPages()
        self.emit(QtCore.SIGNAL('saved'))

    def preview(self):
        if self.previewPost:
            self.previewPost.title=unicode(self.ui.title.text())
            self.previewPost.link=str(self.ui.link.text())
            self.previewPost.text=unicode(self.ui.editor.toPlainText())
            self.previewPost.structured=self.ui.actionRST.isChecked()            
        else:
            self.previewPost=db.PostPreview( postID="PREVIEW%s"%str(time.time()),
                                      title=unicode(self.ui.title.text()),
                                      link=unicode(self.ui.link.text()),
                                      text=unicode(self.ui.editor.toPlainText()), 
                                      structured=self.ui.actionRST.isChecked())
        self.previewPost.render()
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://localhost:8080/preview/%s'%self.previewPost.postID))
