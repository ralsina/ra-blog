# -*- coding: utf-8 -*-

from threading import Thread
import os

class Preview(Thread):
    is_running=False
    def run(self):
        print 'Starting Preview Thread'
        self.cpid=os.spawnlp(os.P_NOWAIT, 'bartleweb.py', 'bartleweb.py')
        print self.cpid
        ret=os.waitpid(self.cpid, 0)
        print 'Ending Preview Thread (%d)'%ret
        self.is_running=False
    def stop(self):
        if self.is_running:
#            os.kill(self.pid)
            pass
        
