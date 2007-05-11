# -*- coding: utf-8 -*-

# Singleton config object

import ConfigParser
import os
from BartleBlog.util.demjson import JSON

conf=ConfigParser.SafeConfigParser()

defaultMenu=[["Home","home","",[]],["Archives","archives","http://www.kde.org",[]],["Tags","tag list","",[]]]


dn=os.path.expanduser('~/.bartleblog/')
if not os.path.isdir(dn):
    os.mkdir(dn)
f=open(os.path.expanduser('~/.bartleblog/config'),'r')
conf.readfp(f)
f.close()

def getValue(section,key,default=None):
    try:
        return JSON().decode(conf.get (section,key))
    except:
        return default

def setValue(section,key,value):
    value=JSON().encode(value)
    try:
        r=conf.set(section,key,value)
    except ConfigParser.NoSectionError:
        conf.add_section(section)
        r=conf.set(section,key,value)
    f=open(os.path.expanduser('~/.bartleblog/config'),'w')
    conf.write(f)
    return r


class ConfigError(Exception):
    def __init__(self,modulename,msg):
        self.modulename=modulename
        self.msg=msg
