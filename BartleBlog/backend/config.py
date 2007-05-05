# -*- coding: utf-8 -*-

# Singleton config object

import ConfigParser
import os

conf=ConfigParser.SafeConfigParser()
    
dn=os.path.expanduser('~/.bartleblog/')
if not os.path.isdir(dn):
    os.mkdir(dn)
f=open(os.path.expanduser('~/.bartleblog/config'),'r')
conf.readfp(f)
f.close()

def getValue(section,key,default=None):
    try:
        return conf.get (section,key)
    except:
        return default

def setValue(section,key,value):
    try:
        r=conf.set(section,key,value)
    except ConfigParser.NoSectionError:
        conf.add_section(section)
        r=conf.set(section,key,value)
    f=open(os.path.expanduser('~/.bartleblog.conf'),'w')
    conf.write(f)
    return r


class ConfigError(Exception):
    def __init__(self,modulename,msg):
        self.modulename=modulename
        self.msg=msg
