# -*- coding: utf-8 -*-

from PyQt4 import QtGui,QtCore

from BartleBlog.ui.Ui_main_config import Ui_Dialog

from BartleBlog.ui.tags_config import TagsConfigWidget
from BartleBlog.ui.pygment_config import PygmentConfigWidget
from BartleBlog.ui.openomy_config import OpenomyConfigWidget
from BartleBlog.ui.blog_config import BlogConfigWidget
from BartleBlog.ui.menu_config import MenuConfigWidget
from BartleBlog.ui.technorati_config import TechnoratiConfigWidget
from BartleBlog.ui.translation_config import TranslationConfigWidget
from BartleBlog.ui.feedburner_config import FeedBurnerConfigWidget

class ConfigWindow(QtGui.QDialog):
    def __init__(self, blog,  page=None):
        QtGui.QDialog.__init__(self)
        self.blog=blog

        # Set up the UI from designer
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.widget=None
        self.widgets={}
        self.layout=QtGui.QHBoxLayout()
        self.ui.frame.setLayout(self.layout)

        # Add configuration items to the list

        QtGui.QListWidgetItem("Blog",self.ui.list)
        self.widgets['blog']=BlogConfigWidget

        QtGui.QListWidgetItem("Tags",self.ui.list)
        self.widgets['tags']=TagsConfigWidget

        QtGui.QListWidgetItem("Blog Menu",self.ui.list)
        self.widgets['blog menu']=MenuConfigWidget

        QtGui.QListWidgetItem("Pygment",self.ui.list)
        self.widgets['pygment']=PygmentConfigWidget

        QtGui.QListWidgetItem("Openomy",self.ui.list)
        self.widgets['openomy']=OpenomyConfigWidget

        QtGui.QListWidgetItem("Technorati",self.ui.list)
        self.widgets['technorati']=TechnoratiConfigWidget

        QtGui.QListWidgetItem("Translations",self.ui.list)
        self.widgets['translations']=TranslationConfigWidget

        QtGui.QListWidgetItem("FeedBurner",self.ui.list)
        self.widgets['feedburner']=FeedBurnerConfigWidget

        QtCore.QObject.connect(self.ui.list,
            QtCore.SIGNAL("currentItemChanged( QListWidgetItem *, QListWidgetItem *)"),
            self.gotoPage)
        if page:
            self.gotoPage(page, page)
    
    def gotoPage(self,current,previous):
        if self.widget:
            self.widget.hide()
            self.widget=None
        pagename=str(current.text()).lower()
        self.widget=self.widgets[str(pagename)](self.blog)
        self.layout.addWidget(self.widget)
