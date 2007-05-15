# -*- coding: utf-8 -*-

from PyQt4 import QtGui,QtCore

import re

empty=128

indented_block_begin=re.compile('^{ \t}*')

blue=QtGui.QTextCharFormat()
blue.setForeground(QtGui.QColor(0,0,0xFF))

class BlockData(QtGui.QTextBlockUserData):
    def __init__(self,position,block):
        QtGui.QTextBlockUserData.__init__(self)
        self.position=position
        self.block=block

class rstHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self,document):
        QtGui.QSyntaxHighlighter.__init__(self,document)
        self.document=document
        QtCore.QObject.connect(self.document,QtCore.SIGNAL('contentsChange(int, int, int)'),self.tagBlock)
        self.rehigh=False

    def tagBlock(self,position,added,removed):
        curBlock=self.document.findBlock(position)
        while True:
            if not unicode(curBlock.text()):
                break
            curBlock.setUserData(BlockData(curBlock.position(),curBlock))
            curBlock=curBlock.next()
        
    def highlightBlock(self,text):
        text=unicode(text)
        blue=QtGui.QTextCharFormat()
        bd=self.currentBlockUserData()
        if bd:
            pos=bd.position
            if pos==0:
                print "00000000000"
                if not self.rehigh:
                    print "rehigh"
                    self.rehigh=True
                    self.rehighlight()
                    self.rehigh=False
            print pos
            blue=QtGui.QTextCharFormat()
            blue.setForeground(QtGui.QColor(0,0,pos))
            self.setFormat(0,len(text),blue)

            
    
        
        
        
        
