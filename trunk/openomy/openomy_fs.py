#!/usr/bin/python


##################################################################################################
#
#   openomyfs v0.1: A FUSE (fuse.sf.net) based file system to mount your Openomy (openomy.com)
#			files on a Linux box.
#
#   v0.3 : CptnAhab     2006-05-20
#       Updated to newer openomy-python interface
#   v0.1 : Manpreet Singh 2006-01-02
#   		First release
#
#   Copyright (C) 2005-2006 Manpreet Singh (manpreet_singh@users.sourceforge.net)
#   Copyright (C) 2006 CptnAhab (cptnahab@gmail.com)
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
#   associated documentation files (the "Software"), to deal in the Software without restriction,
#   including without limitation the rights to use, copy, modify, merge, publish, distribute,
#   sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or substantial
#   portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
#   LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#   WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#   SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
##################################################################################################


import os
from errno import *
from stat import *

from fuse import Fuse

import openomy

import re


class OpenomyFS(Fuse):

    
    def __init__(self, *args, **kw):
            """ Create a new Openomy FS FUSE point. """
    
            Fuse.__init__(self, *args, **kw)
    
            self.user = openomy.User()
    
            self.user.refreshAllTags()
            self.user.refreshAllFiles()
            
            self.rePath = re.compile("(?:/tags/(?P<tagname>[^/]+)(?:/(?P<tagfile>[^/]+))?)|(/(?P<filename>[^/]*))")
    
    
    def _splitpath(self, path):
        # Return a dictionary of path details
        pinfo = {
            "tagname": None,
            "tagfile": None,
            "filename": None
            }
        
        match = self.rePath.match(path)
        if match:
            for key in pinfo:
                pinfo[key] = (match.group(key) and 
                                        match.group(key).strip()
                                        ) or None
                    
        return pinfo["tagname"], pinfo["tagfile"], pinfo["filename"]
    # getattr: called to check for the existence and attributes of a file or a directory,
    #               even before many other operations
    def getattr(self, path):
    
            tagname, tagfile, filename = self._splitpath(path)
    
            # The only two directories: say that they are directories
            if filename == "tags" or (tagname is tagfile is filename is None):
                    return (S_IFDIR | 0755, 0, 0, 2, 0, 0, 0, 0, 0, 0)
    
            # Check for a tag
            elif tagname and tagname in self.user.tags:
                if not tagfile:
                    return (S_IFDIR | 0755, 0, 0, 2, 0, 0, 0, 0, 0, 0)
                    
                # Check for a file within a tag
                tag = self.user.tags[tagname]
                if tagfile in tag.files:
                    file = tag.files[tagfile]
                    if not hasattr(file, 'size'): file.refresh()
                    return (S_IFREG | 0777, 0, 0, 1, 0, 0, int(file.size), 0, 0, 0)
                    
                #else:
                #    return None
    
            # Check for a regular non-directory path
            elif filename:
                if filename in self.user.files:
                    file = self.user.files[filename]
                    if not hasattr(file, 'size'): file.refresh()
                    return (S_IFREG | 0777, 0, 0, 1, 0, 0, int(file.size), 0, 0, 0)
                    
                #else:
                #    return None
               
            e = OSError("No such file "+path)
            e.errno = ENOENT
            raise e
    # Returns the contents of a directory
    def getdir(self, path):
            dirlist = ['.', '..']
    
            tagname, tagfile, filename = self._splitpath(path)
    
            if (path == "/"):
                    dirlist.append('tags')
                    for file in self.user.links("file"):
                            dirlist.append(file.name)
    
            elif (path == "/tags"):
                    for tag in self.user.links("tag"):
                            #print "Tag: %s" % str(tag.__dict__)
                            dirlist.append(tag.name)
    
            # A tag
            elif (path.startswith("/tags")):
                    tagname = path[6:]
                    #print "Tag:", tagname;
                    if tagname in self.user.tags:
                            tag = self.user.tags[tagname]
                            for file in tag.links("file"):
                                    dirlist.append(file.name)
                    else:
                            return -ENOENT
    
            return map(lambda x: (x,0), dirlist)
    
    def rmdir(self, path):
        tagname, tagfile, filename = self._splitpath(path)
        if not tagname:
            return -EPERM
            
        if tagname in self.user.tags:
                self.user.tags[tagname].delete()
                return 0
    
        return -ENOENT
    
    def mkdir(self, path, mode):
        tagname, tagfile, filename = self._splitpath(path)
        
        if not tagname or tagfile or filename:
            return -EPERM
    
        if tagname not in self.user.tags:
            self.user.createTag(tagname)
        
        return 0
        
    
    def mknod(self, path, mode, dev):
        if not S_ISREG(mode) | S_ISFIFO(mode) | S_ISSOCK(mode):
            return -EINVAL
    
        tagname, tagfile, filename = self._splitpath(path)
        
        if filename and filename in self.user.files:
            return 0
        elif tagfile and tagfile not in self.user.files:
            return -1
        elif tagname and tagname not in self.user.tags:
            return -1
        elif not (filename or tagfile):
            return -1
        
        if filename:
            params = { "method": "Files.AddFile" }
            upload_files = [('fileField', filename, "")]
        
            response = openomy.API.dispatch(params,
                                    files=upload_files,
                                    config=self.user.config)
            if not response:
                return -1
        
            # Return the newly created file id.
            fileID = openomy.API.extractId(response, "file id")
        
            # Notify the owner
            self.user._retrieved("file", fileID, filename)
            
        elif tagfile:
            tag = self.user.tags[tagname]
            file = self.user.files[tagfile]
            file.addToTag(tag)
            
        return 0
    
    def open(self, path, flags):
        filename = os.path.basename(path)
        if filename not in self.user.files:
                return -ENOENT
    
        file = self.user.files[filename]
        return 0;
    
    
    def read(self, path, length, offset):
        filename = os.path.basename(path)
        if filename not in self.user.files:
                return -ENOENT;
    
        file = self.user.files[filename]
        filedata = file.getData()
        
        if (length > file.size): length = file.size
    
        return filedata[offset:offset+length]
    
    def write(self, path, buf, off):
        if (path.startswith("/tags/")):
                return len(buf);
        
        # This isn't really correct.
        filename = os.path.basename(path)
        file = self.user.files[filename]
        size = getattr(file, 'size', None)
        if size == 0:
            filedata = ""
        else:
            filedata = file.getData()
    
        filedata = ''.join([
                filedata[:off], buf, 
                filedata[off+len(buf):] ])
        
        params = { "method": "Files.ModifyFile",
                   "fileID": file.id }
        upload_files = [('fileField', filename, filedata)]
        if not openomy.API.dispatch(params, files=upload_files,
                                    config=self.user.config):
            return 0
        
        return len(buf);
    
    def truncate(self, path, size):
        tagname, tagfile, filename = self._splitpath(path)
        
        if (filename and filename not in self.user.files):
            return -1
    
        if tagfile:
            return 0
            
        # Regular file
        file = self.user.files[filename]
        file.size = size
    
        return 0
    
    
    def release(self, path, flags):
        return 0
    
    # Remove a file
    def unlink(self, path):
        
        tagname, tagfile, filename = self._splitpath(path)
        
        if filename and filename not in self.user.files:
            return -ENOENT
        elif tagname and (tagname not in self.user.tags
                or not tagfile or tagfile not in self.user.files):
            return -ENOENT
        
        
        # Removing a file from a tag
        if tagfile:
            tag = self.user.tags[tagname]
            if tagfile not in tag.files:
                    return -ENOENT;
        
            file = tag.files[tagfile]
            file.removeFromTag(tag)
        
        # Removing a regular file
        elif filename:
            self.user.files[filename].delete()
        
        return 0
    
    def link(self, path, path1):
        pass
    



if __name__ == '__main__':

	server = OpenomyFS();
	server.multithreaded = 1;
	server.main();
