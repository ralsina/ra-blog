# -*- coding: utf-8 -*-

# Singleton config object

import ConfigParser
import os

conf=ConfigParser.SafeConfigParser()
fp=open(os.path.expanduser('~/.bartleblog.conf'),'rw')
conf.readfp(fp)
fp.close()

def getValue(section,key,default=None):
    try:
        return conf.get (section,key)
    except:
        return default
        
def setValue(section,key,value):
    try:
        r=conf.set(section,key,value)
    except NoSectionError:
        conf.add_section(section)
        r=conf.set(section,key,value)
    fp=open(os.path.expanduser('~/.bartleblog.conf'),'rw')
    conf.write(fp)
    fp.close()
    return r
    
    
class ConfigError(Exception):
    def __init__(self,modulename,msg):
        self.modulename=modulename
        self.msg=msg
