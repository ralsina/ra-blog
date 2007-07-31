# -*- coding: utf-8 -*-

import os, subprocess

class Preview:
    def __init__(self):
        # FIXME this is pretty hackish
        # See if it's running already
        self.pn=os.path.expanduser('~/.bartleblog')+'/bartleweb.pid'        
        if os.path.exists(self.pn):
            self.pid=int(open(self.pn, 'r').read())
            try:
                os.kill(self.pid, 15)
            except:
                pass
        print "Starting preview process"
        self.pid=subprocess.Popen("bartleweb.py").pid
        open(self.pn, 'w').write(str(self.pid))
    def stop(self):
        print "Killing preview process"
        os.kill(self.pid,  15)
        os.unlink (self.pn)
        pass
        
