# -*- coding: utf-8 -*-

from BartleBlog.ui.editor import EditorWindow
import BartleBlog.backend.dbclasses as db
from PyQt4 import QtGui, QtCore
import time

class StoryEditorWindow(EditorWindow):
    def savePost(self):
        if not self.post:
            self.post=db.Story(postID="BBS%s"%str(time.time()),
                            title=unicode(self.ui.title.text()),
                            link=unicode(self.ui.link.text()),
                            text=unicode(self.ui.editor.toPlainText()))
            # Silly hack to have PostID be unique but not ugly
            self.post.postID='BBS'+str(self.post.id)
        else:
            self.post.title=unicode(self.ui.title.text())
            self.post.link=str(self.ui.link.text())
            self.post.text=unicode(self.ui.editor.toPlainText())
            self.post.render()
        t=unicode(self.ui.tags.text())
        if t:
            cats=[ db.Category.select(db.Category.q.name==c)[0] for c in \
                t.split(',') ]
            self.post.setCategories(cats)
        self.post.render()
        self.post.setDirtyPages()
        self.emit(QtCore.SIGNAL('saved'))
