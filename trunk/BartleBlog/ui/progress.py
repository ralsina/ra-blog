# -*- coding: utf-8 -*-

from PyQt4 import QtGui,QtCore

from BartleBlog.ui.Ui_progress import Ui_Dialog

class ProgressDialog(QtGui.QDialog):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self,parent)

        # Set up the UI from designer
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.stages=[]
        self.gotoStage(0)
        self.setSteps(0)
        self.setPos(0)

    def setSteps(self,n):
        self.ui.progress.setMaximum(n)
        QtCore.QCoreApplication.instance().processEvents()
    def setPos(self,n):
        self.ui.progress.setValue(n)
        QtCore.QCoreApplication.instance().processEvents()
    def step(self,step=1):
        self.ui.progress.setValue(self.ui.progress.value()+step)
        QtCore.QCoreApplication.instance().processEvents()
                
    def gotoStage(self,stage):
        self.curStage=stage
        self.setSteps(0)
        self.setPos(0)
        self.renderStages()
        QtCore.QCoreApplication.instance().processEvents()
        
    def renderStages(self):
        html=''
        for i in range(0,len(self.stages)):
            if i==self.curStage:
               html+='<b>%s</b><br>&nbsp;&nbsp;%s<p>'%(self.stages[i][0],self.stages[i][1])
            else:
               html+='%s<p>'%(self.stages[i][0])
        self.ui.stages.setHtml(html)
        
    def setStages(self,stages):
        self.stages=stages
        self.renderStages()
        
        
        
        
        
        
