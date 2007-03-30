#!/usr/bin/python
""" openomy_update.py - Updater for the python openomy tools.
    @version    0.2
    @summary    This updater automatically downloads the latest 
                version of the openomy tools from the openomy-python.
                googlecode.com/svn/trunk.
    @author       CptnAhab <cptnahab@gmail.com>
    @copyright    (C) 2006-2007 CptnAhab
    @license      Free Software.  See LICENSE.txt for details.
    
"""

# Url opener
import urllib

# Remote file timestamps
import time

# Regular expression matching
import re

# Path manipulation and directory listing
import os, os.path

# Local file timestamps
import stat

# Retrieve the local file listing
curpath = os.getcwd()
curfiles = os.listdir(curpath)

# Retrieve the remote file listing
print "Downloading file list...",
# TODO: Create a stable tag/branch (?)
trunkUrl = "http://openomy-python.googlecode.com/svn/trunk/"
fRSS = urllib.urlopen(trunkUrl)
strRSS = fRSS.read()
fRSS.close()
print "done."

# Extract the remote filelist from the svn filelist
down = 0
reFiles = re.compile("<li><a href=\"[^\"]+\">([^<]+)</a></li>", re.S)
matches = reFiles.findall(strRSS)

# Download each file in the feed
for fname in matches:
    # convert to a struct_time
    if fname == '..': continue
    
    filename = os.path.join(curpath, fname)
    if fname not in curfiles or os.path.isfile(filename):
        print "Downloading %s..." % filename,
        link = trunkUrl + fname
        uret = urllib.urlretrieve(link, filename)
        print "done."
        down += 1
    else:
        print "Cannot overwrite directories or symlinks - %s" % filename

print "Update complete.  Downloaded %i files." % down

