from PyQt4 import QtCore,QtGui

import urllib, os, md5

class PBrowser(QtGui.QTextBrowser):
    
    def loadResource(self, type, name):
        url=unicode(name.toString())
        ret=QtCore.QVariant()
        if url.startswith('http://'):
            dn=os.path.expanduser('~/.bartleblog/cache/')
            if not os.path.isdir(dn):
                os.mkdir(dn)
            m=md5.new()
            m.update(url)
            fn=os.path.join(dn,m.hexdigest())

            print type, fn
            if not os.path.isfile(fn):
                urllib.urlretrieve(url, fn)
            ret=QtGui.QTextBrowser.loadResource(self, type, QtCore.QUrl(fn))
        else:
            ret=QtGui.QTextBrowser.loadResource(self, type, name)
        return ret
