# openomy_test.py
""" openomy_test.py - Testing for the python openomy client and server.
    
    @version    0.1
    @summary    This pretends to be both client and server,
                testing pretty much the entire API.
    @author       CptnAhab <cptnahab@gmail.com>
    @copyright    (C) 2006-2007 CptnAhab
    @license      Free Software.  See LICENSE.txt for details.
    
"""


# WSGI-based Openomy App service
from openomy_server import Service, KirbyObject, StoredFile

# Openomy client
from openomy import Auth, Files, Tags, API, Configuration

# HT without the TP
import urllib2, re, os
from urlparse import urlparse
from rfc822 import unquote
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO




class FakeWSGIServer:
    """ Make-believe WSGI server, for testing. """
    
    defaultEnviron = None
    app = None
    
    requestEnviron = None
    
    responseStatus = None
    responseHeaders = None
    responseOutput = None
    
    def __init__(self, app):
        environ = self.defaultEnviron = dict()
        self.setupTestingDefaults(environ)
        
        self.app = app
        


    
    
    
    def urlopen(self, request):        
        # Convert string urls to Request objects
        if type(request) in (str, unicode):
            request = urllib2.Request(request)
    
        environ = self.requestEnviron = dict(self.defaultEnviron)
        self.responseHeaders = dict()
        self.responseStatus = 500
        self.responseOutput = None
        
        self.parseRequest(request, environ)
        
        self.responseOutput = self.app(environ, 
                 self.handleResponseStart)
                 
        self.responseOutput = ''.join(self.responseOutput)
                             
        return self.Response(request.get_full_url(),
                             self.responseStatus,
                             self.responseHeaders,
                             self.responseOutput)
        
    
    
    
    
    
    def handleResponseStart(self, status, headers):
        responseHeaders = dict(headers)
        self.responseHeaders.update(responseHeaders)
        self.responseStatus = status
        
    
    
    
    
    # Ripped off from cherrypy.wsgiserver.__init__
    
    comma_separated_headers = ['ACCEPT', 'ACCEPT-CHARSET', 'ACCEPT-ENCODING',
        'ACCEPT-LANGUAGE', 'ACCEPT-RANGES', 'ALLOW', 'CACHE-CONTROL',
        'CONNECTION', 'CONTENT-ENCODING', 'CONTENT-LANGUAGE', 'EXPECT',
        'IF-MATCH', 'IF-NONE-MATCH', 'PRAGMA', 'PROXY-AUTHENTICATE', 'TE',
        'TRAILER', 'TRANSFER-ENCODING', 'UPGRADE', 'VARY', 'VIA', 'WARNING',
        'WWW-AUTHENTICATE']
    
    quoted_slash = re.compile("(?i)%2F")
    
    def parseRequest(self, request, environ):
        """Parse the next HTTP request start-line and message-headers."""
    
        environ["REQUEST_METHOD"] = request.get_method()
        
        path = request.get_full_url()
        scheme, location, path, params, qs, frag = urlparse(path)
    
        environ["wsgi.url_scheme"] = scheme
    
        environ["SERVER_NAME"] = location
        if ':' in location:
            l, environ["SERVER_PORT"] = location.split(":", 1)
    
        if params:
            path = path + ";" + params
        
        atoms = [unquote(x) 
                 for x in self.quoted_slash.split(path)]
        path = "%2F".join(atoms)
        environ["PATH_INFO"] = path
    
        environ["QUERY_STRING"] = qs
        
        # then all the http headers
        for k, v in request.header_items():
            k, v = k.strip().upper(), v.strip()
            envname = "HTTP_" + k.replace("-", "_")
            
            if (k in self.comma_separated_headers 
                and envname in environ):
                v = ", ".join(environ[envname], v,)
            environ[envname] = v
            
        ct = environ.pop("HTTP_CONTENT_TYPE", None)
        if ct: environ["CONTENT_TYPE"] = ct
        environ.pop("HTTP_CONTENT_LENGTH", None)
    
        bodyData = request.get_data()
        if bodyData is None: bodyData = ""
        environ['wsgi.input'] = StringIO(bodyData)
        environ['CONTENT_LENGTH'] = len(bodyData)
        environ['wsgi.input'].length = environ['CONTENT_LENGTH']
    
    
    
    
    # Ripped off from Python2.5 wsgiref.util
    def setupTestingDefaults(self, environ):
    
        environ.setdefault("SERVER_SOFTWARE", "Fake WSGI Server")
        environ.setdefault('SERVER_NAME','127.0.0.1')
        environ.setdefault('SERVER_PROTOCOL','HTTP/1.0')
    
        environ.setdefault('HTTP_HOST',environ['SERVER_NAME'])
        environ.setdefault('REQUEST_METHOD','GET')
    
        if 'SCRIPT_NAME' not in environ and 'PATH_INFO' not in environ:
            environ.setdefault('SCRIPT_NAME','')
            environ.setdefault('PATH_INFO','/')
    
        environ.setdefault('wsgi.version', (1,0))
        environ.setdefault('wsgi.run_once', 0)
        environ.setdefault('wsgi.multithread', 0)
        environ.setdefault('wsgi.multiprocess', 0)
    
        from StringIO import StringIO
        environ.setdefault('wsgi.input', StringIO(""))
        environ.setdefault('wsgi.errors', StringIO())
        environ.setdefault('wsgi.url_scheme', "HTTP")
    
        if environ['wsgi.url_scheme']=='http':
            environ.setdefault('SERVER_PORT', '80')
        elif environ['wsgi.url_scheme']=='https':
            environ.setdefault('SERVER_PORT', '443')
    
    
    
    
    
    class Response(StringIO):
        responses = BaseHTTPRequestHandler.responses
        
        def __init__(self, url, status, headers, output):
                
            StringIO.__init__(self, output)
    
            self.url = url
            statuscode, msg = status.split(" ", 1)
            self.status = int(statuscode)
            self.msg = msg
            self.headers = headers
    
            if self.status >= 300 or self.status < 200:
                print output
                raise urllib2.HTTPError(self.url, 
                                    self.status,
                                    self.msg,
                                    self.headers,
                                    self)
        
        
        def geturl():
            return self.url
    
    
    




class Debug:
    """ Various debugging functions. """
    
    
    
    def CreateApplication(cls, name=None, version=None, 
                          description=None, ownerID=None, 
                          config=None):
    
        if name is None: 
            appName = API.getConfigParam('appName', config)
        if version is None: 
            version = API.getConfigParam('appVersion', config)
        if description is None: 
            description = API.getConfigParam('appDescription', config)
        if ownerID is None: 
            ownerID = API.getConfigParam('appOwnerID', config)
        
        params = { "method": "Debug.CreateApplication",
                   "name": name,
                   "version": version,
                   "description": description,
                   "ownerID": ownerID }
        
        response = API.dispatch(params, config=config, cfm=False)
        if not response:
            return False
    
        appKey = API.extract(response, "<applicationKey>", 
                                 "</applicationKey>")
        privKey = API.extract(response, "<privateKey>", 
                                 "</privateKey>")
                                 
        return (appKey, privKey)
    
    CreateApplication = classmethod(CreateApplication)    
    
    def Reinitialize(cls, config=None):
    
        params = { "method": "Debug.Reinitialize" }
        
        response = API.dispatch(params, config=config, cfm=False)
        if not response:
            return False
    
        return True
    
    Reinitialize = classmethod(Reinitialize)
    


### Test setup

# Specialized configuration
myConfig = Configuration(path="./testing",
                         name="openomy-test.ini",
                         default=True)
myConfig.save(format=Configuration.FORMAT_INI)


# Application info
myConfig.set("appName", "openomy_test")
myConfig.set("appVersion", "1.0")
myConfig.set("appDescription", "Openomy Client/Server Testing Application")
myConfig.set("appOwnerID", 0)

# Server info
myConfig.set("apiBase", "http://localhost:9009/openomy")

# TODO: Create some data files for uploading



# Create a fake WSGI server
wsgiServer = FakeWSGIServer(Service())

# Create a fake urlopener
API.urlopen = wsgiServer.urlopen

# Set up the server testing environment
wsgiServer.defaultEnviron['OPENOMY_APP_ROOT'] = '/openomy'
tblPath = KirbyObject.PATH = './testing/tables'
if not os.path.exists(tblPath):
    os.makedirs(tblPath)
filePath = StoredFile.PATH = './testing/files'
if not os.path.exists(filePath):
    os.makedirs(filePath)


# Debug.Reinitialize: Delete everything.
Debug.Reinitialize()


### Account testing

# Debug.CreateApplication: Get a new application key.
appKey, privKey = Debug.CreateApplication()
    
myConfig.set('applicationKey', appKey)
myConfig.set('privateKey', privKey)

# Auth.RegisterUser: Register a User and Session
myConfig.set("username", "testuser")
myConfig.set("password", "testing123")
myConfig.set("email", "test@example.com")
cfmToken = Auth.RegisterUser()

# Auth.AuthorizeUser: Authorize a User Session
cfmToken = Auth.AuthorizeUser()
myConfig.set('confirmedToken', cfmToken)

# Save the config info
myConfig.save()




### Begin File testing

# Files.GetAllFiles: Get a list of User's Files
files = Files.GetAllFiles()
if len(files) > 0:
    raise "Too many files: expecting 0, received %i" % len(files)

# Files.AddFile: Upload a File
fileAdded = Files.AddFile(filename="openomy_test.py")
if fileAdded is False:
    raise "File upload failure."

# Files.GetAllFiles: Get a list of User's Files
files = Files.GetAllFiles()
if len(files) != 1:
    raise "Wrong number of files: expecting 1, received %i" % len(files)

fileID = files[0][1]
fileName = files[0][2]
    
# Files.GetFile: Retrieve a File's info
file = Files.GetFile(fileID=fileID)
if file is False:
    raise "Failed to GetFile '%s'." % fileName


# Download: Retrieve a File's contents
downurl = "%(baseurl)s?fileToken=%(filetoken)s" % file
contents = wsgiServer.urlopen(downurl).read()
if contents != open(fileName).read():
    raise "Contents don't match!"
    

# Files.ModifyFile: Overwrite a File
if not Files.ModifyFile(fileID=fileID,
                        filename='./testing/openomy-test.ini'):
    raise "File modification failure."

# Files.GetFile: Retrieve a File's info
file = Files.GetFile(fileID=fileID)

# Download: Retrieve a File's contents
fileName = "./testing/openomy-test.ini"
downurl = "%(baseurl)s?fileToken=%(filetoken)s" % file
contents = wsgiServer.urlopen(downurl).read()
if contents != open(fileName).read():
    raise "Contents don't match!"

# Files.DeleteFile: Remove a File and its contents
if not Files.DeleteFile(fileID=fileID):
    raise "File deletion failure."

# Files.GetAllFiles: Get a list of Users's Files
files = Files.GetAllFiles()
if len(files) != 0:
    raise "Wrong number of files: expecting 0, received %i" % len(files)






### Tag testing

# Tags.GetAllTags: Get a list of User's Tags
tags = Tags.GetAllTags()
if len(tags) > 0:
    raise "Too many tags: expecting 0, received %i" % len(tags)


# Tags.CreateTag: Create a Tag for a User
tag = Tags.CreateTag(tagName="test-tag")
if tag is False:
    raise "Failed to create tag 'test-tag'."

# Tags.GetAllTags: Get a list of User's Tags
tags = Tags.GetAllTags()
if len(tags) < 1:
    raise "Wrong number of tags: expecting 1, received %i" % len(tags)

tagID = tags[0][1]
tagName = tags[0][2]

# Files.AddFile: Add a File, with a Tag
fileAdded = Files.AddFile(filename="openomy_test.py", tagID=tagID)
if fileAdded is False:
    raise "File upload failure."
    
files = Files.GetAllFiles()
if len(files) != 1:
    raise "Wrong number of files: expecting 1, received %i" % len(files)

fileID = files[0][1]
fileName = files[0][2]

# Tags.GetTag: Get a list of Users and Files for a Tag
tag = Tags.GetTag(tagID)
if tag is False:
    raise "Failed to retrieve tag '%s'." % tagName

if len(tag['files']) != 1:
    print "Tag: %s" % str(tag)
    raise "Wrong number of files: expecting 1, received %i" % len(tag['files'])

# Tags.DeleteFileFromTag: Remove a File from a Tag
if not Tags.DeleteFileFromTag(tagID, fileID):
    print "Tag: %s" % str(tag)
    raise "Failed to remove file from tag."

# Tags.AddFileToTag: Add a File to a Tag
if not Tags.AddFileToTag(tagID, fileID):
    print "Tag: %s" % str(tag)
    raise "Failed to re-add file to tag."

# Tags.GetTag: Get a list of Users and Files for a Tag
tag = Tags.GetTag(tagID)
if tag is False:
    raise "Failed to retrieve tag '%s'." % tagName

# Tags.DeleteTag: Remove a Tag
if not Tags.DeleteTag(tagID):
    print "Tag: %s" % str(tag)
    raise "Failed to delete tag '%s'." % tagName


### Finish file testing


# Files.GetAllFiles: Get a list of Users's Files
files = Files.GetAllFiles()
if len(files) != 1:
    raise "Wrong number of files: expecting 1, received %i" % len(files)
    
# Files.DeleteFile: Remove a File and its contents
if not Files.DeleteFile(files[0][1]):
    raise "Failed to delete file '%s'." % files[0][2]

# Files.GetAllFiles: Get a list of Users's Files
files = Files.GetAllFiles()
if len(files) != 0:
    print str(files)
    raise "Wrong number of files: expecting 0, received %i" % len(files)


### ALL DONE
print "Passed all tests."


