# -*- coding: utf-8 -*-

# Singleton config object

import ConfigParser
import os
from BartleBlog.util.demjson import JSON

defaultMenu=[["Home","home","",[]],["Archives","archives","",[]],["Tags","tag list","",[]]]

def getValue(section,key,default=None):
    section=section.lower()
    key=key.lower()
    try:
        return JSON().decode(conf.get (section,key))
    except:
        return default

def setValue(section,key,value):
    section=str(section)
    key=str(key)
    section=section.lower()
    key=key.lower()
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


conf=ConfigParser.SafeConfigParser()
firstRun=False
dn=os.path.expanduser('~/.bartleblog/')
if not os.path.isdir(dn):
    os.mkdir(dn)
if not os.path.isfile(os.path.expanduser('~/.bartleblog/config')):
    open(os.path.expanduser('~/.bartleblog/config'),'w').close()
    firstRun=True
f=open(os.path.expanduser('~/.bartleblog/config'),'r')
conf.readfp(f)
f.close()



