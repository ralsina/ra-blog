#!/usr/bin/python
""" openomy-python: Python bindings for the Openomy REST API

    @version    0.5
    @license    Free Software.  See LICENSE.TXT for details.
    @copyright  Copyright (C) 2005-2006 Manpreet Singh 
                    <manpreet_singh@users.sourceforge.net>
    @copyright  Copyright (C) 2006-2007 CptnAhab 
                    <cptnahab@gmail.com>

    Version History
    ===============
    v0.5 : CptnAhab 2007-02-07
         Integrated AutoLoginUser and AutoRegisterUser
            into User, added Configuration items
         Re-throws Server Exceptions
         Tested with Python Server and FUSE bindings
         Fixed RFC1891 request packing
    v0.4 : CptnAhab 2006-05-20
         Added Auth.AuthorizeUser and
            Auth.RegisterUser
    v0.2 : CptnAhab 2006-03-19
         Slight refactoring
    v0.1 : Manpreet Singh 2006-01-02
         First release

    TODO
    ===============
    * Unit tests
    * Deferred responses from API
    * Logging integration?
"""

# Basic imports
import os, sys

# For GET and POST requests
import urllib, urllib2

# For file uploading (fileup)
import mimetools, mimetypes

# For fileup and local caching
import time

# For file downloading and local caching
import calendar

# For opening the authorization link
import webbrowser

# For signing messages
import md5

# YAML configuration processing
try:
    import yaml
except ImportError:
    yaml =  None

# INI configuration processing
import ConfigParser    

# for locating SYSCONF
import platform

# For regex-style parsing
import re



# Define error codes/messages.

ERR_UNKNOWN = -1
ERR_BAD_TOKEN = 0
ERR_BAD_SIG = 1
ERR_UNAUTHORIZED = 2
ERR_MISSING_ARG = 3
ERR_BAD_FILETAG = 4
ERR_BAD_TAG = 5
ERR_BAD_USER = 6
ERR_OVER_QUOTA = 7
ERR_MAX_QUOTA = 8
ERR_BAD_APP_KEY = 9
ERR_BAD_METHOD = 10


class OpenomyError(Exception):
    MESSAGES = {
        ERR_UNKNOWN: "Unknown error",
        ERR_BAD_TOKEN: "Invalid token",
        ERR_BAD_SIG: "Invalid signature",
        ERR_UNAUTHORIZED: "Permissions",
        ERR_MISSING_ARG: "Null Reference",
        ERR_BAD_FILETAG: "General",
        ERR_BAD_TAG: "Tag Name Not Valid",
        ERR_BAD_USER: "User Not Found",
        ERR_OVER_QUOTA: "File Too Large",
        ERR_MAX_QUOTA: "Out Of Storage",
        ERR_BAD_APP_KEY: "Invalid Application Key",
        ERR_BAD_METHOD: "Unknown Method"
        }
    
    CODES = dict([ (v, k) for k, v in MESSAGES.items()])
    
    def __init__(self, errCode):
        self.code = errCode
        self.message = self.MESSAGES[self.code]
        self.args = [self.message]
        







class DefaultConfiguration:
    """ A simple namespace class for hard-coded
    default API configuration. """

    # The hard-coded default server info.  This is
    # the URL portion before "/api".
    apiBase = "http://www.openomy.com"     # For default server
    # apiBase = "http://localhost:9009"    # For local stand-alone server
    # apiBase = "http://localhost/openomy" # For local mod_python server
    
    # The hard-coded default application details
    appName = "Openomy-Python Client"
    appVersion = "0.5"
    appDescription = "Python client for accessing Openomy API endpoints."
    appOwnerID = 0
    
    # The hard-coded default application key,
    # private key, and confirmed token.  Private
    # keys and confirmed tokens MUST NOT be
    # accessible to anyone but the app owner.
    applicationKey = '1e31cb69be8d30070f7607b4f23d4f95'
    privateKey = '39578658'
    confirmedToken = None
    
    
    # The hard-coded default username, password
    # and e-mail.  You probably don't want these in
    # the source code, but here's a spot just in
    # case.
    username = None
    password = None
    email = None

    
    
    def get(cls, attr):
        """ Retrieve a configuration parameter """
        return cls.__dict__.get(attr, None)
    get = classmethod(get)    
    def set(cls, attr, val):
        """ Set a configuration parameter """
        cls.__dict__[attr] = val
        return val
    set = classmethod(set)





class Configuration:
    """ Simple openomy configuration management.
    Stores configuration in-memory and persists to
    a specified location, in either Yaml or INI. """

    FORMAT_ANY = -1
    if yaml:
        FORMAT_DEF = 1
    else:
        FORMAT_DEF = 2
    FORMAT_YAML = 1
    FORMAT_INI = 2
    
    # this is the correct case because
    # INI is case insensitive in attr
    # names
    ATTR_NAMES = ( "applicationKey",
                   "privateKey",
                   "confirmedToken",
                   "username",
                   "password",
                   "email",
                   "appName",
                   "appDescription",
                   "appVersion",
                   "appOwnerID",
                   "apiBase" )
    ATTR_KEYS = [k.lower() for k in ATTR_NAMES]
    
    _path = None
    _name = "openomy"
    _values = None
    

    def __init__(self, path=None, name=None, default=False):  
        """ Create a new configuration object. """
        self._path = path
        self._name = name
        self._values = dict()
        if default:
            API.userConfig = self
    def get(self, attr):
        """ Retrieve a configuration parameter """
        return self._values.get(attr, None)
    def save(self, path=None, name=None, format=FORMAT_DEF):
        """ Store the configuration directives
        for APP or USER to a file. """
        
        if format not in (Configuration.FORMAT_YAML, 
                          Configuration.FORMAT_INI):
            # Set the format
            format = Configuration.FORMAT_DEF
    
        # Make sure we have a path
        if not path:
            path = self._path or os.getcwd()
        
        # Make sure the path exists        
        if not os.path.isdir(path):
            # This will raise an exception for us
            os.makedirs(path)
        
        # Make sure we have a name
        if not name:
            name = self._name or Configuration._name
        
        ext = os.path.splitext(name)[1]
        if ext == "":
            ext = [ "", ".yml", ".ini" ][format]
        else:
            ext= ""
            
        filename = os.path.join(path, name)
        if not os.path.exists(filename):
            # Add an extension if we can
            filename += ext
    
        if format == Configuration.FORMAT_YAML:
            if yaml:
                
                yfile = file(filename, "w")
                
                # write in alpha order
                keys = self._values.keys()
                keys.sort()
                for key in keys:
                    yline = "%s: %s\n" % (key, self._values[key])
                    yfile.write(yline)
                
                yfile.close()
                
            else:
                format = Configuration.FORMAT_INI
    
        if format == Configuration.FORMAT_INI:
            ifile = file(filename, "w")
            
            # write the header
            ifile.write("[Openomy]\r\n")
            
            # write in alpha order
            keys = self._values.keys()
            keys.sort()
            for key in keys:
                iline = "%s=%s\r\n" % (key, self._values[key])
                ifile.write(iline)
            
            ifile.close()
            
        return True
    def set(self, attr, val):
        """ Set a configuration parameter """
        strval = str(val)
        self._values[attr] = strval
        if not attr.startswith("_"):
            # for easy attribute access
            setattr(self, attr, strval) 
        return val
    def load(self, path=None, name=None, format=FORMAT_ANY):
        """ Load the configuration directives
        for APP or USER from a file. """
        
        if format not in (Configuration.FORMAT_YAML,
                            Configuration.FORMAT_INI,
                            Configuration.FORMAT_ANY):
            # Set the format
            format = Configuration.FORMAT_DEF
        
        if not path:
            path = self._path or os.getcwd()
                
        if not name:
            name = self._name
            if not name:
                name = Configuration._name
            
        filename = os.path.join(path, name)
        if not os.path.exists(filename):
            exts = {}
            if format in (Configuration.FORMAT_ANY,
                          Configuration.FORMAT_INI):
                exts[Configuration.FORMAT_INI] = ".ini"
            if format in (Configuration.FORMAT_ANY,
                          Configuration.FORMAT_YAML):
                exts[Configuration.FORMAT_YAML] = ".yml"
            
            tried = [filename]
            basename = filename
            found = None
            for format, ext in exts.items():
                filename = basename + ext
                if os.path.exists(filename):
                    found = filename
                    break
                else:
                    tried.append(filename)
        
            if not found:
                # SOL
                print "Could not locate file to load. Attempted:"
                for t in tried:
                    print "\t%s" % t
                return False
    
        if format in (Configuration.FORMAT_YAML,
                      Configuration.FORMAT_ANY):
            tyaml = file(filename).read()
            config = yaml.load_document(tyaml)
            if not isinstance(config, dict):
                print "Invalid YAML configuration."
                print "Document must be a map."
            
            else:
                # We succeeded.
                format = Configuration.FORMAT_YAML
    
        if format in (Configuration.FORMAT_INI,
                      Configuration.FORMAT_ANY):
            
                # Use the ini loader
                cparser = ConfigParser.ConfigParser()
                cparser.read(filename)
                config = cparser.items("Openomy")
                if not isinstance(config, list):
                    print "Invalid INI configuration file."
                    return False
    
                config = dict(config)
                
                # Clean up the attribute names    
                outConfig = dict()
                for key, val in config.items():
                    try:
                        # see if it should be normalized
                        nKey = self.ATTR_KEYS.index(key)
                        key = self.ATTR_NAMES[nKey]
                    except ValueError:
                        # leave it alone
                        continue
                    outConfig[key] = val
                       
                config = outConfig
    
        # Remember the config data we just loaded
        for key in config:
            self.set(key, config[key])
        return config







class _API:
    """ Implements the REST api calling mechanism. """

    REST = "/api/rest/"
    DOWNLOAD = "/api/download/"
    LOGIN = "/api/login/"
    
    config = DefaultConfiguration
    
    # Holds default user configuration
    userConfig = None
    
    # Overridable urlopen (as per Google In-Stall Pamphlet)
    urlopen = staticmethod(urllib2.urlopen)
    
    def __getattr__(self, name):
        """ Check for capwords/uscore notation """
        
        # Python attribute name trickery
        # automatically finds "getTag" when you 
        # use ob.GetTag or ob.get_tag
        if name[0] != name[0].lower():
            return getattr(self, name[0].lower() + name[1:])
        elif "_" in name:
            name = re.sub(r'_([a-z])', lambda m: (m.group(1).upper()), name)
            return getattr(self, name)
        else:
            raise AttributeError, name
    
    def sign(self, params, config=None, cfm=True):
        """ sign a list of parameters after applying
        keys and tokens """
    
        # Get the appKey and privateKey
        appKey = self.getConfigParam('applicationKey', config)
        privKey = self.getConfigParam('privateKey', config)
                
        if not (appKey and privKey):
            # can't sign without those
            return False
    
        params['applicationKey'] = appKey
    
        # Get the confirmedToken
        if cfm:
            cfmToken = self.getConfigParam('confirmedToken', config)
    
            if not cfmToken:
                # can't do that, either
                return False
    
            params['confirmedToken'] = cfmToken
       
        # Create a signature
        keylist = params.keys()
        keylist.sort()
        sigdat = "".join([ "%s=%s" % (str(k), str(params[k]))
                           for k in keylist ])
        sigdat += privKey
        sig = md5.new(sigdat).hexdigest()
    
        params['signature'] = sig
        return sig
    
    
    
    def getUrl(self, params, baseurl=REST, config=None, cfm=True):
        """ Encode a GET request url """
        lclparms = dict(params)
        
        signed = self.sign(lclparms, config=config, cfm=cfm)
        if cfm and not signed:
            return False
    
        apiBase = self.getConfigParam('apiBase', config)
        url =  apiBase + baseurl + "?" + urllib.urlencode(lclparms)       
        #print "URL: %s" % url
        return url
    
    
    
    # From: http://berserk.org/uploadr/
    
    def getRequest(self, params, url, files, config=None, cfm=True):
        """ Build a POST request """
    
        # Collect our thoughts before the journey
        lclparms = dict(params)
        signed = self.sign(lclparms, config=config, cfm=cfm)
        if cfm and not signed:
            return False
    
    
        # Create the MIME boundary text
        bound = '-----'+mimetools.choose_boundary()+'-----'
        
        # Grow the body inch by inch, line by line
        L = list()    
        
        # Add the form parameters
        for key in lclparms:
            L.append('--' + bound)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(lclparms[key])
        
        # Add the files
        for (key, filename, value) in files:
            filetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            L.append('--' + bound)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % filetype)
            L.append('')
            L.append(value)
    
        # Close the MIME envelope
        L.append('--' + bound + '--')
        L.append('')
    
        # Form a single body string
        body = '\r\n'.join(L)
    
        # And generate the request object.
        headers = dict()
        headers['Content-type'] = 'multipart/form-data; boundary=' + bound
        headers['Content-length'] = str(len(body))
        
        apiBase = self.getConfigParam('apiBase', config)
        return urllib2.Request(apiBase + url, body, headers)
    
    
    
    
    def getConfigParam(self, paramName, config=None):
        """ Retrieve a param value from one of the three
        possible configuration sources. """
        
        for cfg in (config, self.userConfig, self.config):
            if not cfg: continue
    
            paramValue = cfg.get(paramName)
            if paramValue is not None:
                break
                
        return paramValue
        
    
    
    
    def dispatch(self, params, 
                 baseurl=REST, 
                 files=None, 
                 config=None,
                 cfm=True):
        """ Dispatch an API request to the server. """
    
        if files:
            # POST em
            req = self.getRequest(params, baseurl, files, config=config, cfm=cfm)
            urlopen = _API.urlopen
            f = urlopen(req)
            response = f.read()
            
        else:
            # GET it
            url = self.getUrl(params, baseurl, config=config, cfm=cfm)
            urlopen = _API.urlopen
            f = urlopen(url)
            response = f.read()
            
        # Failure implies failure.
        if not self.succeeded(response):
            errCode = self.getError(response)
            raise OpenomyError(errCode)
            
        return response
    
    
    
    def succeeded(self, response):
        return -1 != response.find("<success>")
    
    
    def getError(self, response):
        errName = self.extract(response, "<error>", "</error>")
        errName = errName.strip()
        if errName in OpenomyError.CODES:
            return OpenomyError.CODES[errName]
        return -1
    
    
    def extract(self, haystack, beforeneedle, afterneedle):
        """ Extract a needle from the haystack string 
            based on the surrounding context """
            
        pos1 = haystack.find(beforeneedle) + len(beforeneedle)
        pos2 = haystack.find(afterneedle, pos1)
        return haystack[pos1:pos2]
        
    
    
    def extractObjects(self, response, tagname=None):
        # Find any objects at all.
        # groups: 1-type, 2-id, 3-name
        robj = re.compile('<(?P<tag>.+) id="([^"]+)"[^>]*>([^<]*)</(?P=tag)>', re.I)
    
        # somewhere to put our objects
        objects = list()
    
        # Do the match (the monster match)
        matches = robj.findall(response)
        for ob in matches:
            # only match tagname
            if tagname and ob[0] != tagname:
                continue
            objects.append(ob)
        
        return objects
    
    
    
    def extractFields(self, response):
        """ Extract <tag attrs>data</tag> from
        an Openomy response. """
    
        # Find any field at all
        robj = re.compile("<(?P<tag>[^>]+)\s?(\S+?)?>(.*)</(?P=tag)>", re.I)
    
        # Find all of the fields
        matches = robj.findall(response)
        fields = dict()
        for match in matches:
            tag, text = match[0], match[2]
            # TODO: xml attrs - group 1
            fields[tag] = text
        
        return fields
    
    
    
    def extractId(self, response, id_string):
        """ Pull out an id attribute. """
    
        pos1 = response.find(id_string)
        id0 = pos1 + len(id_string) + 2
        id1 = response.find('"', id0)
        
        return response[id0:id1]    
    
    

API = _API()







class _Auth:
    """ Methods to make sure that only the 
    right users and applications can talk 
    to each other. """
    
    def __init__(self, API):
        self.API = API
        
    
    def RegisterUser(self, username=None, 
                                password=None, 
                                email=None,
                                config=None):
        """ Register a new user account on Openomy. """
    
        # Check the various levels of config
        if not username:
            username = API.getConfigParam('username', config)
        if not password:
            password = API.getConfigParam('password', config)
        if not email:
            email = API.getConfigParam('email', config)
    
        params = { "method": "Auth.RegisterUser",
                   "username": username,
                   "password": password,
                   "email": email }
    
        response = API.dispatch(params, cfm=False, config=config)
        if not response:
            return False
    
        return API.extract(response, "<confirmedtoken>", 
                                 "</confirmedtoken>")
    
    
    
    def AuthorizeUser(self, username=None, 
                                password=None,
                                config=None):
        """ Obtain a confirmed token for the user. """
    
        # Check the various levels of config
        if not username:
            username = API.getConfigParam('username', config)
        if not password:
            password = API.getConfigParam('password', config)
    
        params = { "method": "Auth.AuthorizeUser",
                   "username": username,
                   "password": password }
    
        response = API.dispatch(params, cfm=False, config=config)
        if not response:
            return False
    
        return API.extract(response, "<confirmedtoken>", 
                                 "</confirmedtoken>")
    
    
    
    def GetUnconfirmedToken(self, config=None):
        """ Initiate a session for an application. """
        
        params = { "method": "Auth.GetUnconfirmedToken" }
    
        response = API.dispatch(params, cfm=False, config=config)
        if not response:
            return False
    
        return API.extract(response, "<unconfirmedtoken>", 
                                 "</unconfirmedtoken>")
    
    
    
    def GetConfirmedToken(self, uncfmToken, config=None):
        """ Attempt to obtain a confirmedToken
        authorizing access to a user account. """
    
        params = { "method": "Auth.GetConfirmedToken",
                   "unconfirmedToken": uncfmToken }
    
        response = API.dispatch(params, cfm=False, config=config)
        if not response:
            return False
            
        cfmToken = API.extract(response, "<confirmedtoken>", 
                                     "</confirmedtoken>")
    
        return cfmToken
    
    

Auth = _Auth(API)





class _Files:
    """ Methods to perform actions on files. """
    
    def __init__(self, API):
        self.API = API
        
    
    def GetFile(self, fileID, timeout=None, config=None):
        """ Load the details about a file from 
        Openomy, and obtain a download link. """
        
        params = { "method": "Files.GetFile",
                   "fileID": fileID }
        
        if timeout:
            params["timeout"] = timeout
        
        response = API.dispatch(params, config=config)
        if not response:
            return False
        
        # Collect the attributes from the response
        fileinfo = API.extractFields(response)
    
        # Keep the id
        fileinfo["id"] = fileID
    
        # Get the size units
        fileinfo["sizeunits"] = API.extract(response,
                            '<size units="', '">')
        
        return fileinfo
    
    
    
    def AddFile(self, filename, tagID=None, config=None):
        """ Create a file on openomy from the local
        file 'filename'. """
                                
        params = { "method": "Files.AddFile" }
        if tagID:
            params['tagID'] = tagID
    
        upload_files = [('fileField',
                        os.path.basename(filename),
                        file(filename, 'rb').read())]
    
        response = API.dispatch(params,
                                files=upload_files,
                                config=config)
        if not response:
            return False
    
        # Return the newly created file id.
        return API.extractId(response, "file id")
    
    
    
    def DeleteFile(self, fileID, config=None):
        """ Deletes the given file from Openomy. """ 
        
        params = { 'method': "Files.DeleteFile",
                   'fileID': fileID }
    
        return not not API.dispatch(params, config=config)
    
    
    
    def ModifyFile(self, fileID, filename, config=None):
        """ Create a file on openomy from the local
        file 'filename'. """
       
        params = { "method": "Files.ModifyFile",
                   "fileID": fileID }
    
        upload_files = [('fileField',
                        os.path.basename(filename),
                        file(filename, 'rb').read())]
    
        return not not API.dispatch(params,
                                    files=upload_files,
                                    config=config)
    
    
    
    def GetAllFiles(self, config=None):
        """ Retrieve all the files for a user. """
    
        params = { "method":  "Files.GetAllFiles" }
    
        response = API.dispatch(params, config=config)
        if not response:
            return False
    
        return API.extractObjects(response, "file")
    
    
    

Files = _Files(API)




class _Tags:
    """ Methods to perform actions on tags. """
    
    def __init__(self, API):
        self.API = API
    
    
    def GetAllTags(self, config=None):
        """ Retrieves a list of all the tags for a user.
        This includes tags the user has created as well 
        as tags the user was invited to (and accepted). 
        """
    
        params = { "method":  "Tags.GetAllTags" }
    
        response = API.dispatch(params, config=config)
        if not response:
            return False
    
        return API.extractObjects(response, "tag")
    
    
    
    
    def GetTag(self, tagID, config=None):
        """ Gets information, including the name, 
        the date created, the files within, the 
        id, etc. about the tag in question. """
        
        params = { "method": "Tags.GetTag",
                   "tagID": tagID }
    
        response = API.dispatch(params, config=config)
        if not response:
            return False
            
        rtag = re.compile('<tag\s+id="([^"]+?)"\s+name="([^"]+?)"\s+created="([^"]+?)"\s*>', re.I)
        tag = dict()
    
        # Do the match (the monster match)
        matches = rtag.findall(response)
        for groups in matches:
            tag["id"] = groups[0]
            tag["name"] = groups[1]
            tag["created"] = groups[2]
    
        # TODO: extract the attributes
        tag["files"] = API.extractObjects(response, "file")
        # TODO: extract the attributes
        tag["users"] = API.extractObjects(response, "user")
    
        return tag
    
    
    
    
    def CreateTag(self, tagName, config=None):
        """ Creates a new tag associated with a user. """
        
        params = { "method": "Tags.CreateTag",
                   "tagName": tagName }
    
        response = API.dispatch(params, config=config)
        if not response:
            return False
            
        return API.extractId(response, "tag id")
    
    
    
    def DeleteTag(self, tagID, config=None):
        """ Deletes a tag if the user is an admin
        or creator of the tag. """
    
        params = { "method": "Tags.DeleteTag",
                   "tagID": tagID }
            
        return not not API.dispatch(params, config=config)
    
    
    
    def AddFileToTag(self, tagID, fileID, config=None):
        """ Adds a file to a specific tag. """
    
        params = { "method": "Tags.AddFileToTag",
                   "tagID": tagID,
                   "fileID": fileID }
    
        return not not API.dispatch(params, config=config)
    
    
    
    
    
    def DeleteFileFromTag(self, tagID, fileID, config=None):
        """ Deletes a file from a specific tag. """
        
        params = { "method": "Tags.DeleteFileFromTag",
                   "tagID": tagID,
                   "fileID": fileID }
                 
        return not not API.dispatch(params, config=config)
    
    

Tags = _Tags(API)
class RemoteProxy:
    """ Base type for proxying remote objects
    belonging to some master object. """
    _owner = None
    _remote = None
    _loaded = False
    
    def __init__(self, owner, refresh=True, **kwargs):
        self._owner = owner
        if not self._remote:
            self._remote = dict()
        self.__dict__.update(kwargs)
        if refresh:
            self.refresh()
    
    
    def __getattr__(self, name):
        """ Check for capwords/uscore notation """
        
        # Python attribute name trickery
        # automatically finds "getTag" when you 
        # use ob.GetTag or ob.get_tag
        if name[0] != name[0].lower():
            return getattr(self, name[0].lower() + name[1:])
        elif "_" in name and not name[0] == "_":
            name = re.sub(r'_([a-z])', lambda m: (m.group(1).upper()), name)
            return getattr(self, name)
        else:
            raise AttributeError, name
    
    def links(self, linktype):
        if linktype not in self._remote:
            return
        
        done = list()
        index = self._remote[linktype][0]
        for link in index:
            if index[link] not in done:
                done.append(index[link])
                yield index[link]
    
    def refresh(self):
        """ Placeholder. """
        self._loaded = False
        return False
    def _updated(self, obtype, obdefs):
        """ Notifies the object that its collection
        contents have been updated. """
    
        if obtype not in self._remote:
            # we don't care.
            return False
    
        # What are we comparing to?
        remobs = dict(self._remote[obtype][0])
    
        # Add the new objects
        ret = list()
        for tobj in obdefs:
            # Prevent the object from being filtered
            # later
            if tobj[1] in remobs:
                rem = remobs[tobj[1]]
                del remobs[rem.id]
                if rem.name in remobs:
                    del remobs[rem.name]
    
            # Get/create and notify everyone
            obj = self._retrieved(*tobj)
            if self != obj._owner:
                self._added(obj)
                obj._added(self)
                
            # return it later
            ret.append(obj)
        
        # Remove the old objects that weren't reloaded
        removed = []
        for key in remobs.keys():
            oldob = remobs[key]
            if oldob.id not in removed:
                removed.append(oldob.id)
                # notification
                self._removed(oldob)
                oldob._removed(self)
    
        # Return all the objects we obtained.
        return ret
    
    
    def _retrieved(self, obtype, obid, obname):
        """ Respond to an object retrieval with
        a local RemoteProxy construction. """
        
        # Make sure the owner object is the master
        if self._owner and self != self._owner:
            return self._owner._retrieved(obtype, obid, obname)
           
        # Make sure we have a constructor, etc.
        if obtype not in self._remote:
            return False
        
        # Create or find the object
        
        klass = self._remote[obtype][1]
        obdict = self._remote[obtype][0]
        
        if obid not in obdict:
            ob = klass(self._owner, 
                       refresh=False,
                       id=obid, 
                       name=obname)
    
            self._added(ob)
            ob._added(self)
        else:
            ob = obdict[obid]
            if obname != ob.name:
                obname, ob.name = ob.name, obname
                self._renamed(ob, obname)
    
        return ob
    def _added(self, object):
        """ Notification of an object added to
        this collection. """
    
        # Make sure we store this type
        obtype = object.__class__.__name__
        if obtype not in self._remote:
            return False
        
        # Look up the klass name into a tag name
        obtype = self._remote[obtype]
            
        # Store under both id and name
        self._remote[obtype][0][object.id] = object
        self._remote[obtype][0][object.name] = object
    
        return True
    
    def _renamed(self, object, oldname):
        """ Notification that a collected object
        has been renamed. """
        
        # Make sure we store this type
        obtype = object.__class__.__name__
        if obtype not in self._remote:
            return False
    
        # Look up the klass name into a tag name
        obtype = self._remote[obtype]
            
        # Remove the old name reference
        del self._remote[obtype][0][oldname]
        
        # Insert a new name reference
        self._remote[obtype][0][object.name] = object
    
        return True
    
    def _removed(self, object):
        """ Notification of an object removed from
        this collection. """
    
        # Make sure we store this type
        obtype = object.__class__.__name__
        if obtype not in self._remote:
            return False
            
        # Turn the klass name into a tag name
        obtype = self._remote[obtype]
    
        # Make sure we have stored the object
        if object.id not in self._remote[obtype][0]:
            return False
    
        # Remove all references    
        del self._remote[obtype][0][object.id]
        del self._remote[obtype][0][object.name]
        
        return True
    

class User(RemoteProxy):
    """ A user (master) proxy object. """
    tags = None
    files = None
    partners = None
    config = None
    default = True
    authLevel = -1
    
    homedir = os.path.expanduser("~")
    configdir = os.path.join(homedir, ".openomy")
    
    def __init__(self, default=True, 
                       config=True,
                       auth=True,
                       refresh=True):
        """ Create a user remote proxy """
        
        self.tags = dict()
        self.files = dict()
        self.partners = dict()
        self._remote = { "tag": (self.tags, Tag),
                        "Tag": "tag",
                        "file": (self.files, File),
                        "File": "file",
                        "user": (self.partners, Partner),
                        "Partner": "user" }
        self.config = dict()
        self.default = default
        
        if config:
            self.loadConfig()
        
        if auth:
            auth = self.obtainAccess()
    
        if (self.authLevel & 3) != 3:
            refresh = False
    
        RemoteProxy.__init__(self, self, refresh=refresh)
    def obtainAccess(self):
        """ Obtain authorization to access Openomy. """
        
        lauth = self.checkAuthLevel()
        
        # We have no keys.
        if (lauth & 2) == 0:
            return self.obtainAppCreds()
            
        # We have no login or confirmed token.
        elif (lauth & 5) == 0:
            return self.obtainCfmToken()
    
        # We have no confirmed token
        elif (lauth & 1) == 0:
            return self.obtainAppAuth()
    
        # We already have everything.    
        else:
            return True
    def loadConfig(self):
        """ Load the user configuration info. """
     
        parms = { "path": self.configdir }
        if self.default:
            parms["default"] = True
    
        self.config = Configuration(**parms)
        return self.config.load(format=Configuration.FORMAT_ANY)
    def refresh(self):
        """ Do a couple of things. """
        
        self.getAllFiles()
        self.refreshAllTags()
        self._loaded = True
    def refreshAllTags(self):
        """ Reload the tag list, and then the file 
        list and other info for each tag. """
        
        tags = self.getAllTags()
        if not tags:
            return False
            
        success = True
        for tag in tags:
            if not tag.refresh():
                success = False
                # oh god don't stop.
                
        return success
    def refreshAllFiles(self):
        """ Reload the file list, and then the file 
        info for each one. """
        
        files = self.getAllFiles()
        if not files:
            return False
            
        success = True
        for file in files:
            if not file.refresh():
                success = False
                # oh god don't stop.
                
        return success
    def checkAuthLevel(self):
        """ See what sort of authorization we need
        to do with Openomy. """
    
        keys = 0
        token = 0
        login = 0
        appKey, privKey, cfmToken, userName, password = (None,) * 5
        for item in (self.config, API.config):
    
            if not appKey:
                appKey = item.get('applicationKey')
            if not privKey:
                privKey = item.get('privateKey')
            if not cfmToken:
                cfmToken = item.get('confirmedToken')
            if not userName:
                userName = item.get('username')
            if not password:
                password = item.get('password')
            
            # check that appkey and privkey are validish
            if not (isinstance(appKey, (str, unicode))
                    and len(appKey) == 32) or \
               not (isinstance(privKey, (str, unicode))
                    and len(privKey) == 8):            
                item.set('applicationKey', None)
                item.set('privateKey', None)
            else:
                keys = 2
                
            # check that cfmtoken is validish
            if not (isinstance(cfmToken, (str, unicode))
                    and len(cfmToken) == 40):
                # Not valid cfmToken
                item.set('confirmedToken', None)
            else:
                token = 1
                
            # check that the login is validish
            if not (isinstance(userName, (str, unicode))
                and isinstance(password, (str, unicode))):
                item.set('userName', None)
                item.set('password', None)
            else:
                login = 4
    
    
        if (self.authLevel < keys + token + login and 
            self.authLevel != -1):
            self.config.save()
    
        self.authLevel = keys + token + login
        return self.authLevel
    def obtainAppCreds(self):
        """ Obtain a full set of credentials for the
        application. """
    
        # Get an unconfirmed token first
        appToken = Auth.RegisterApplication()
        if not appToken:
            print "Could not get an application token"
            return False
    
        # Prompt the user to authorize 
        # the app in the browser and respond back
        result = None
        while self.promptToAuthorize(app=appToken):
    
            # Try to obtain the keys and token
            result = Auth.GetApplicationCredentials(appToken)
            if result:
                break
    
        if not result:
            print "Could not get application credentials"
            return False        
            
        appkey, privkey, cfmToken = result
        self.config.set('applicationKey', appkey)
        self.config.set('privateKey', privkey)
        self.config.set('confirmedToken', cfmToken)
        self.checkAuthLevel()
        return True
    def obtainAppAuth(self):
        """ Obtain a confirmed token for the
        application using a username and password. """
        
        userName, password, email = None, None, None
        for item in (self.config, API.config):
            if not userName:
                userName = item.get('username')
            if not password:
                password = item.get('password')
            if not email:
                email = item.get('email')
                
    
        # Get an confirmed token first
        try:
            if email and not userName:
                cfmToken = Auth.AuthorizeUser(email, password,
                                          config=self.config)
            else:
                cfmToken = Auth.AuthorizeUser(userName, password,
                                          config=self.config)
        except OpenomyError, f:
            if f.code == ERR_BAD_USER and (username and
                password and email):
                
                cfmToken = Auth.RegisterUser(userName, password,
                                  email, config=self.config)
                        
            else:
                print "Could not login as user"
                raise                              
    
        self.config.set('confirmedToken', cfmToken)
        self.checkAuthLevel()
        return True
    def obtainCfmToken(self):
        """ Obtain a confirmed token for a user who
        already has application/private keys """
    
        # Get an unconfirmed token first
        uncfmToken = Auth.GetUnconfirmedToken()
        if not uncfmToken:
            print "Could not get an unconfirmed token"
            return False
    
        # Prompt the user to authorize 
        # the app in the browser and respond back
        cfmToken = None
        while self.promptToAuthorize(uncfm=uncfmToken):
            
            # Try to obtain a confirmed token
            cfmToken = Auth.GetConfirmedToken(uncfmToken)
            if cfmToken:
                break
    
        if not cfmToken:
            print "Could not get a confirmed token"
            return False        
            
        self.config.set('confirmedToken', cfmToken)
        self.checkAuthLevel()
        return True
    def promptToAuthorize(self, app=None, uncfm=None):
        """ Open the authorization URL in a web
        browser, and wait for user confirmation. """
    
        # where to go?
        if app:
            params = { 'appToken': app }
        else:
            params = { 'unconfirmedToken': uncfm }
        url = API.getUrl(params, baseurl=API.LOGIN, cfm=False)
    
        # open the browser
        webbrowser.open(url)
        
        # inform the user on the console
        print "Please authenticate at the following url." + \
              "This will allow this application access " + \
              "to your Openomy account:"
              
        print "\n" + url + "\n\n"
        
        # wait for a key press
        ans = raw_input("Press Enter to recheck " + \
                        "confirmation or Ctrl+C " + \
                        "to quit.")
                        
        return True
    def addFile(self, localsrc, tag=None):
        """ Adds a file to a users openomy account,
        tagged with the optional tag. """
    
        params = dict()
        if tag:
            params['tagID'] = tag.id
    
        fileID = Files.AddFile(localsrc,
                               config=self.config,
                                **params)
    
        filename = os.path.basename(localsrc)
    
        # Notify the owner
        ofile = self._retrieved("file", fileID, filename)
        if tag:
            tag._added(ofile)
            ofile._added(tag)
        
        return ofile
    def createTag(self, name):
        """ Create a new Tag object. """
        
        tagID = Tags.CreateTag(name, config=self.config)
    
        # Notify the owner
        return self._retrieved("tag", tagID, name)
    def getAllFiles(self):
        """ Retrieve a list of file objects for
        this user. """
        
        files = Files.GetAllFiles(config=self.config)
        return self._updated("file", files)
    def getAllTags(self):
        """ Retrieve a list of tag objects for
        this user. """
        
        tags = Tags.GetAllTags(config=self.config)
        return self._updated("tag", tags)

class Partner(RemoteProxy):
    """ This class represents another user on
    openomy.  You can't act as them, so there
    isn't much here but a data leaf. """
    tags = None
    files = None
    
    
    def __init__(self, owner, refresh=True, **kwargs):
        self.tags = dict()
        self.files = dict()
        
        self._remote = { "tag": (self.tags, Tag),
                         "Tag": "tag",
                         "file": (self.files, File),
                         "File": "file" }
                
        
        RemoteProxy.__init__(self, owner, refresh, **kwargs)
    def refresh(self):
        pass

class Tag(RemoteProxy):
    """ A tag on openomy. """
    files = None
    partners = None
    
    def __init__(self, owner, refresh=True, **kwargs):
        """ Create a new Tag remote proxy. """
    
        self.files = dict()
        self.partners = dict()
        self._remote = { "file": (self.files, File),
                         "File": "file",
                         "user": (self.partners, Partner),
                         "Partner": "user" }
    
        RemoteProxy.__init__(self, owner, refresh, **kwargs)
    def refresh(self):
        """ Retrieve the list of files that this
        tag has been applied to. """
        
        taginfo = Tags.GetTag(tagID=self.id,
                   config=self._owner.config)
    
        if not taginfo:
            return False
            
        # Save other attributes
        for attr in taginfo:
            if attr not in ("tags", "files", "partners"):
                setattr(self, attr, taginfo[attr])
            
        # Save our file list
        self._updated("file", taginfo["files"])
        self._updated("user", taginfo["users"])
    
        self._loaded = True
        return True
    def delete(self):
        """ Delete this tag from openomy. """
        
        if not Tags.DeleteTag(tagID = self.id,
                   config = self._owner.config):
            return False
    
        # Notify any local files we're tagging        
        for file in self.files:
            file._removed(self)
            
        # Notify the user so we can uncache, etc.
        self._owner._removed(self)
        
        # Remove our id.
        del self.id
        
        return True
    def addFile(self, file):
        """ Attach this tag to a file """
        if file.id in self.files:
            return True
    
    
        if not Tags.AddFileToTag(fileID=file.id,
                                  tagID=self.id,
                       config=self._owner.config):
            return False
        
        # Add the file to our list
        self._added(file)
        # Vice versa
        file._added(self)
        
        return True
    def deleteFile(self, file):
        """ Remove this tag from the file. """
        if file.id not in self.files:
            return False
    
        if not Tags.DeleteFileFromTag(tagID=self.id,
                                   fileID = file.id,
                         config = self._owner.config):
            return False
    
        # Remove the file from our list       
        self._removed(file)
        # Vice versa
        file._removed(self)
        
        return True

class File(RemoteProxy):
    tags = None
    partners = None
    
    def __init__(self, owner, refresh=True, **kwargs):
        """ Create a new File remote proxy. """
    
        self.tags = dict()
        self.partners = dict()
        self._remote = { "tag": (self.tags, Tag),
                         "Tag": "tag",
                         "user": (self.partners, Partner),
                         "Partner": "user" }
    
        RemoteProxy.__init__(self, owner, refresh, **kwargs)
    def refresh(self, timeout=10):
        """ Load the file information and open
        the file window temporarily. """
    
        fileinfo = Files.GetFile(fileID=self.id,
                                timeout=timeout,
                     config = self._owner.config)
                    
        if not fileinfo:
            return False
    
        for attr in fileinfo:
            if attr not in ("tags", "files", "partners"):
                setattr(self, attr, fileinfo[attr])
        
        for attr in ('modified', 'created'):
            setattr(self, attr, time.strptime(fileinfo[attr], "%m/%d/%Y %H:%M:%S %p"))
            
        self._loaded = True
    
        return fileinfo
    def delete(self):
        """ Remove this file completely. """
    
        if not Files.DeleteFile(self.id,
              config=self._owner.config):
            return False
    
        # Notify any local tags
        for tag in self.tags:
            tag._removed(self)
    
        # Notify the user    
        self._owner._removed(self)
        
        # Make sure we don't try something stupid
        del self.id
        
        return True
    def getUrl(self):
        """ Retrieve the url for downloading this file. """
    
        if not self._loaded:
            if not self.refresh():
                return False
    
        params = { "fileToken": self.filetoken }
    
        return API.getUrl(params, baseurl=API.DOWNLOAD)
    def getData(self):
        """ Retrieve the contents of the file """
    
        url = self.getUrl()    
        if not url:
            return None
            
        f = urllib.urlopen(url)
        fileData = f.read()
        return fileData
    def download(self, filename):
        """ Write a local file with our contents. """
        
        fileData = self.getData()
        if fileData is None:
            return False
        
        # save the data
        here = file(filename, 'wb')
        here.write(fileData)
        here.close()
        
        # set the modification stamp
        mtime = calendar.timegm(self.modified)
        os.utime(filename, (mtime, mtime))
        return True
    def upload(self, filename, refresh=True):
        """ Upload a local file's contents over ours. """
        
        if not self.ModifyFile(fileID = self.id,
                            filename = filename,
                    config = self._owner.config):
            return False
    
        # We're outta date.
        self._loaded = False
        
        if refresh:
            self.refresh()
    
        return True
    # 
    # These next two simply delegate to the Tag class
    # 
    
    
    
    def addToTag(self, tag):
        """ Add this file to a tag. """
        if tag.id in self.tags:
            return True
        
        return tag.addFile(self)
    def removeFromTag(self, tag):
        """ Remove a tag from this file. """
        if tag.id not in self.tags:
            return False
    
        return tag.deleteFile(self)
