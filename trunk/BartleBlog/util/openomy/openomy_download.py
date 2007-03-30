#!/usr/bin/python
"""  openomy-download.py - openomy-python example

This openomy python example downloads the contents
of your Openomy account to a local directory, skipping any
pre-existing files.

This is just an example.  For better synchronization, use
openomy-sync.py. """

import os, os.path
import openomy

# For debugging.
#import urllib
#proxies = {'http': 'http://localhost:8080/'}
#urllib._urlopener = urllib.FancyURLopener(proxies)

# ~/Openomy will be the destination.
destdir = os.path.join(os.path.expanduser("~"), "Openomy")
if not os.path.exists(destdir):
  os.makedirs(destdir)

# Get a local file list
files = os.listdir(destdir)


# The openomy.User object automatically 
# manages the user login, keys, and tokens.
# Settings will be automatically loaded from 
# and saved to "~/.openomy/openomy.ini"
# NOTE: YAML support requires PyYAML 3000 
# This will check openomy.yml.
# We don't want to load the tag list, just 
# download files.  So, no auto-refresh.
print "Logging in..."
u = openomy.User(refresh=False)

# Refresh and sort the remote file list

print "Retrieving remote file listing..."
rfiles = u.GetAllFiles()
for nfile in range(len(rfiles)):
  rfiles[nfile] = (rfiles[nfile].name, rfiles[nfile])
rfiles.sort()


print "Downloading to %s..." % destdir
for fname, ofile in rfiles:  
  if ofile.name not in files:
    print "Downloading %s..." % ofile.name
    filename = os.path.join(destdir, ofile.name)
    ofile.download(filename)
    print "\tdone."
  else:
    print "Skipping %s...already exists.\n" % ofile.name

print "All done!"

