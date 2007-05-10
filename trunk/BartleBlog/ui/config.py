# -*- coding: utf-8 -*-

from PyQt4 import QtGui,QtCore

from BartleBlog.ui.Ui_main_config import Ui_Dialog

from BartleBlog.ui.tags_config import TagsConfigWidget
from BartleBlog.ui.pygment_config import PygmentConfigWidget
from BartleBlog.ui.openomy_config import OpenomyConfigWidget
from BartleBlog.ui.blog_config import BlogConfigWidget
from BartleBlog.ui.menu_config import MenuConfigWidget

class ConfigWindow(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

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

        QtCore.QObject.connect(self.ui.list,
            QtCore.SIGNAL("currentItemChanged( QListWidgetItem *, QListWidgetItem *)"),
            self.gotoPage)

    def gotoPage(self,current,previous):
        if self.widget:
            self.widget.hide()
            self.widget=None
        pagename=str(current.text()).lower()
        self.widget=self.widgets[str(pagename)]()
        self.layout.addWidget(self.widget)
