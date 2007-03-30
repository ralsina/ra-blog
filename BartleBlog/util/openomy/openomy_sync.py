#!/usr/bin/python
""" openomy-sync.py - Openomy Account and Tag synchronizer

    @summary      Facilitates synchronization between a
                  local directory and a remote Openomy
                  account or tag(s).
    @version      0.3 - Implemented login and registration capabilities
    @author       CptnAhab <cptnahab@gmail.com>
    @copyright    (C) 2006 CptnAhab
    @license      Free Software.  See LICENSE.txt for details.
    
"""

import openomy
import os, os.path
import stat, time
import optparse # requires python2.3+

DIR_DOWN = -1
DIR_BOTH = 0
DIR_UP = 1


class OpenomySync:
    """ A class responsible for synchronizing a folder
        with an openomy account or tag.
    
        @ivar direction:  Whether synchronization is to be
                          Up-only (DIR_UP), Down-only
                          (DIR_DOWN), or both
                          (DIR_BOTH).
        @ivar user:       The openomy.User object whose account
                          is to be sync'ed.
                        
    """
    
    def __init__(self, direction=DIR_BOTH, username=None, password=None, email=None):
      """ Create an openomy synchronizer object. """
      self.direction = direction
        
      if username or password or email:
        self.user = openomy.User(auth=false, refresh=false)
        if username:
            self.user.config['username'] = username
        if password:
            self.user.config['password'] = password
        if email:
            self.user.config['email'] = email
        
        if self.user.obtainAccess():
            self.user.refresh()
        
      else:
        self.user = openomy.User()
        
      if self.user.authLevel != 7:
        raise "Could not authorize access."
    def getRemoteFileList(self, tag=None):
      """ Retrieve a list of remote file tuples (id, obj)
      from either a tag or the whole account. """
    
      filesrc = self.user
      if tag:
        if hasattr(tag, 'files'):
          filesrc = tag
        else:
          # we'll assume it's a string with a tagname.
          filesrc = self.user.tags[tag]
    
      filesrc.refresh()
    
      # Retrieve the actual list of files
      rfiles = dict()
      for key in filesrc.files:
        rfile = filesrc.files[key]
        if rfile.name not in rfiles:
            rfiles[rfile.name] = rfile
      rfiles = rfiles.items()
      rfiles.sort()
    
          
      # print "Files: %s" % str(rfiles)
        
    
      return rfiles
    def upload(self, filename, tag=None, exists=False):
      """ Add a local file to the Openomy user account. """
      
      if self.direction > DIR_DOWN:
        # ok to upload
        if not exists:
          self.user.addFile(filename, tag=tag)
        else:
          file = self.user.files[os.path.basename(filename)]
          file.upload(filename, False)
        return True
      return False
    def download(self, rfile, filename):
      """ Download the openomy.File file data
      into the local file specified by filename. """
      
      if self.direction < DIR_UP:
        # ok to download
        rfile.download(filename)
        # set the timestamp!!!!
        if not rfile._loaded:
          rfile.refresh()
          rModTime = calendar.timegm(rFile.modified)
          os.utime(filename, (rModTime, rModTime)) 
        return True
      return False
    def sync(self, directory, tag=None, verbose=True):
      """ Synchronize a local folder with a
      remote tag or personal file list. """
        
      # Make sure we have a tag object
      if tag and not hasattr(tag, 'id'):
        if tag not in self.user.tags:
            # Create the tag automagically
            self.user.createTag(tag)
        tag = self.user.tags[tag]
    
      # Get the remote list
      lRemote = self.getRemoteFileList(tag)
    
      # Get the local list
      lLocal = os.listdir(directory)
      lLocal.sort()
    
      # Walk the list and find missing items
      MARKER = "\xFF"
      nUp, nDown, nLocal, nRemote = 0, 0, 0, 0
      while (nLocal <= len(lLocal) and nRemote <= len(lRemote)) and not \
            (nLocal >= len(lLocal) and nRemote >= len(lRemote)):
        
        if nLocal >= len(lLocal):
          strLocal = MARKER
        else:
          strLocal = lLocal[nLocal]
        
        if nRemote >= len(lRemote):
          strRemote = MARKER
        else:
          strRemote = lRemote[nRemote][0]
    
    
        if strLocal < strRemote:
          # strLocal is not on remote
          filename = os.path.join(directory, strLocal)
          if not os.path.isfile(filename):
            print "\t\tSkipping subfolder %s" % filename
          else:
            # upload it
            if verbose:
              print "\t\tUploading %s" % strLocal
            if self.upload(filename, tag):
              nUp += 1
          # check the next local file
          nLocal += 1
    
        elif strRemote < strLocal:
          # strRemote is not on local
          if verbose:
            print "\t\tDownloading %s" % strRemote
          
          filename = os.path.join(directory, strRemote)
          if self.download(lRemote[nRemote][1], filename):
            nDown += 1
    
          # check the next remote file
          nRemote += 1
    
        else:
          # They're the same filename.  Which one is newer?
          # TODO: cache the most recent modified stamp for
          # each remote file. (ick)
          filename = os.path.join(directory, strLocal)
          if not os.path.isfile(filename):
            print "\t\tSkipping subfolder %s" % filename
          else:
            lFile = os.stat(filename)
            lSize =lFile[stat.ST_SIZE]
            lModStamp = time.localtime(lFile[stat.ST_MTIME])
    
            rFile = lRemote[nRemote][1]
            rFile.refresh()
            rSize = int(rFile.size)
            rModStamp = rFile.modified
            
            # File size is irrelevant, but helpful for
            # debugging the timestamps.
            if lSize != rSize:
              if lModStamp > rModStamp:
                # Local file is newer.  Upload.
                if verbose:
                  print "\t\tUploading %s" % strLocal
                if self.upload(filename, tag, exists=True):
                  nUp += 1
              else:
                # Remote file is newer.  Download.
                if verbose:
                  print "\t\tDownloading %s" % strLocal
                if self.download(rFile, filename):
                  nDown += 1
            else:
              print "\t\tSkipping %s" % strLocal
    
          nLocal += 1
          nRemote += 1
    
      return nUp, nDown

if __name__ == "__main__":

    # Construct the command line argument handling
    oparser = optparse.OptionParser()
    
    # These options are only to get the confirmed token
    # i.e. first run only.
    oparser.add_option("-a", "--acct", dest="user",
                        help="authenticate with account USER", metavar="USER")
    oparser.add_option("-p", "--pass", dest="passwd",
                        help="authenticate with password PASS", metavar="PASS")
    oparser.add_option("-e", "--email", dest="email",
                        help="register new user with email EMAIL", metavar="EMAIL")
                        
    # This option allows you to synchronize the current folder
    # with a specific single tag
    oparser.add_option("-t", "--tag", dest="tag",
                        help="synchronize with TAG", metavar="TAG")
    
    # This option allows you to specify the base folder to use
    # if not the current folder
    oparser.add_option("-b", "--base", dest="base",
                        help="set base directory for synchronization to BASE", metavar="BASE")
    
    
    # These options allow you to synchronize in only one direction
    oparser.add_option("-d", "--download", dest="direction", action="store_const",
                        help="download only; do not upload anything.", const=DIR_DOWN)
    oparser.add_option("-u", "--upload", dest="direction", action="store_const",
                        help="upload only; do not download anything.", const=DIR_UP)
    oparser.set_default('direction', DIR_BOTH)
    
    # TODO: Options for excluding or including certain files
    #       Let's look at tar, cpio, etc.
    
    # Parse the command line
    (options, args) = oparser.parse_args()

    
    # For debugging.
    #import urllib2
    #proxies = {'http': 'http://localhost:8888/'}
    #proxy_handler = urllib2.ProxyHandler(proxies)
    #opener = urllib2.build_opener(proxy_handler)
    #urllib2.install_opener(opener)
    
    
    # args should be a list of directories to synchronize
    # with their eponymous tags, or empty to synchronize the current
    # directory with your personal root file store.
    print "Logging in to Openomy..."
    s = OpenomySync(options.direction, options.user,
                    options.passwd, options.email)
    
    # Normalize the optional base sync directory
    basedir = os.path.abspath(os.path.normpath(options.base or ""))
    
    if len(args) == 0:
      # synchronize file store
      print "Synchronizing account to %s..." % basedir
      up, down = s.sync(basedir, options.tag)
      print "Synchronization complete. Files: Up %i  Down %i" % (up, down)
    
    else:
      # synchronize a list of tags
      ttlup, ttldown = 0, 0
      print "Synchronizing specified tags to %s..." % basedir
      for arg in args:
        dirname = os.path.join(basedir, arg)
        if not os.path.exists(dirname):
          os.makedirs(dirname)
        if not os.path.isdir(dirname):
          print "%s is not a folder."
          continue
    
        print "\tSynchronizing tag %s..." % arg
        up, down = s.sync(dirname, arg)
        print "\tTag synchronization complete. Files: Up %i  Down %i" % (up, down)
        ttlup += up ;  ttldown += down
      print "Synchronization complete. Files: Up %i  Down %i" % (ttlup, ttldown)