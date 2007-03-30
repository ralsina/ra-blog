#!/usr/bin/env python
""" openomy_server: Python Server for the Openomy REST/Download API

    @version    0.1
    @license    Free Software.  See LICENSE.TXT for details.
    @copyright  API Copyright (C) 2005-2006 Openomy LLC
    @copyright  Server Copyright (C) 2006-2007 CptnAhab 
                    <cptnahab@gmail.com>

    Version History
    ===============
    v0.1 : CptnAhab 2007-02-07
         Supports standard API methods, as well as
                some Debug.* methods
         Runs under Paste as standalone or using 
                Apache mod_python
         Relocatable from root via environment var
         
         

    TODO
    ===============
    * New Url.* management methods
    * Switchable storage back-ends
        * SQLite
        * MySQL
        * PostgreSQL
    * Switchable access front-ends
        * S3 API
        * GData Storage API
    * Unit tests from openomy_test
"""

# Error handling
from paste.httpexceptions import HTTPExceptionHandler, HTTPNotFound
from paste.exceptions.errormiddleware import ErrorMiddleware
from paste.translogger import TransLogger

# Request, Response objects
from paste.wsgiwrappers import WSGIRequest, WSGIResponse

# Root url mapping
from paste.urlmap import URLMap

# Database service
from kirbybase import KirbyBase, KBError
import os, os.path

# Record timestamps
import datetime

# Random id generation
import random

# Key generation
import md5, sha




# KirbyDB table/object abstraction

class KirbyObject:
    VALTYPES = { 
        "str": "String", 
        "float": "Float",
        "bool": "Boolean", 
        "int": "Integer",
        "datetime": "DateTime",
        "date": "Date" 
        }
    
    PATH = "~/.openomy/server/tables/"
    PATH = os.path.expanduser(PATH)
        
    # Basic properties    
    created = datetime.datetime.today()
    modified = datetime.datetime.today()

    def getTableName(cls):
        if not os.path.exists(cls.PATH):
            os.makedirs(cls.PATH)
        return os.path.join(cls.PATH, cls.__name__)
    getTableName = classmethod(getTableName)

    def tabledef(klass, parent=None):
        # Search the parent klass
        if parent:
            ptabledef = parent.tabledef
        else:
            ptabledef = ()
        
        if callable(ptabledef): 
            ptabledef = ptabledef(parent)
            
        attrs = list(ptabledef)
        for attr, val in klass.__dict__.items():
            if attr[:1] == "_": continue  # Skip volatile attributes
            valtype = type(val).__name__
            valtype = KirbyObject.VALTYPES.get(valtype, None)
            if valtype:
                attrs.append(":".join((attr,valtype)))
        attrs.sort()
        return tuple(attrs)
    tabledef = staticmethod(tabledef)
    
    def select(cls, db, fields=None, vals=None, single=False):
        table = cls.getTableName()
        if not getattr(cls, 'exists', False): cls.ensureTableExists(db)
        if not fields: fields = cls.keys
        if not vals: 
            raise ValueError, "No vals specified for select."
        result = db.select(table, fields, vals, returnType='dict')
        ret = list()
        for record in result:
            instance = cls.instance(**record)
            instance._db = db
            if single: return instance
            ret.append(instance)
        return tuple(ret)
    select = classmethod(select)

    def instance(cls, **data):
        obj = cls()
        obj.__dict__.update(data)
        return obj
    instance = classmethod(instance)    

    def newInstance(cls, **kwargs):
        obj = cls.instance(**kwargs)
        obj.setCreated()
        obj.setModified()
        return obj
    newInstance = classmethod(newInstance)
    
    def getNewKey(cls, db):
        obid = ObjectID.select(db, vals=[cls.__name__], single=True)
        if obid == tuple():
            obid = ObjectID.instance()
            obid.table = cls.__name__
            newRec = True
        else:
            newRec = False
        obid.cur += 1
        obid.setModified()
        if not newRec:
            obid.update(db)
        else:
            obid.insert(db)
        return obid.cur
    getNewKey = classmethod(getNewKey)
    
    def setCreated(self):
        self.created = datetime.datetime.today()
        
    def setModified(self):
        self.modified = datetime.datetime.today()
        
    def getKeys(self, fields=None):
        if not fields and hasattr(self, 'recno'):
            keys, keyvals = ['recno'], [self.recno]
        else:
            keys = fields or self.keys
            keyvals = [ getattr(self, key) for key in keys ]
        return keys, keyvals
    
    def insert(self, db):
        self._db = db or self._db
        if not getattr(self, 'exists', False): self.ensureTableExists(self._db)
        for key in self.keys:
            if not getattr(self, key, None):
                setattr(self, key, self.getNewKey(self._db))
        self.recno = db.insert(self.getTableName(), self)
        args = (self.getTableName(),) + self.getKeys()
        recvals = self._db.select(returnType='dict', *args)[0]
        self.__dict__.update(recvals)
        return self.recno
        
    def delete(self, db=None):
        self._db = db or self._db
        if not getattr(self, 'exists', False): self.ensureTableExists(self._db)
        args = (self.getTableName(),) + self.getKeys()
        return (1 == self._db.delete(*args))            
        
    def update(self, db=None):
        self._db = db or self._db
        if not getattr(self, 'exists', False): self.ensureTableExists(self._db)
        args = (self.getTableName(),) + self.getKeys() + (self, )
        return 1 == self._db.update(*args)

    def createTable(cls, db):
        return db.create(cls.getTableName(), list(cls.tabledef))
    createTable = classmethod(createTable)
               
    def dropTable(cls, db):
        if os.path.exists(cls.getTableName()):
            return db.drop(cls.getTableName())
        return True
    dropTable = classmethod(dropTable)
        
    def initTable(cls, db):
        rows = []
        if hasattr(cls, 'initRecs'):
            for row in cls.initRecs:
                rowDict = map(cls.tabledef, row)
                rows.append(cls.newInstance(db=db, **rowDict))
        return rows
    initTable = classmethod(initTable)
    
    def ensureTableExists(cls, db):
        if not os.path.exists(cls.getTableName()):
            cls.createTable(db)
        cls.exists = True
    ensureTableExists = classmethod(ensureTableExists)









class StoredFile:

    PATH = "~/.openomy/server/files/"
    PATH = os.path.expanduser(PATH)
    
    fileID = 0
    name = ""
        
    def getFullPath(self):
        return os.path.join(self.PATH, self.name)
        
    def getData(self):
        return file(self.getFullPath(), "r").read()
        
    def setData(self, data):
        if not os.path.exists(self.PATH):
            os.makedirs(self.PATH)
        storedFile = file(self.getFullPath(), "w")
        bytes = storedFile.write(data)
        storedFile.close()
        return bytes
        
    def instance(cls, file):
        storedFileName = "o%05i.f%05i.data" % (file.ownerID, file.fileID)
        obj = cls()
        obj.name = storedFileName
        obj.fileID = file.fileID
        obj.file = file
        return obj
    instance = classmethod(instance)
    
    def delete(self):
        return os.unlink(self.getFullPath())
        









class ObjectID(KirbyObject):
    """ Similar to SQL-extension "SERIAL" (PG) or 
    "AUTO_INCREMENT" (My). """
    # Keys
    table = ""

    # Props
    min = 1
    step = 1
    max = 32768
    cur = 0

    
ObjectID.tabledef = KirbyObject.tabledef(ObjectID, KirbyObject)
ObjectID.keys = ['table']







class Application(KirbyObject):
    """ A client of the Openomy API. """
    
    # Keys
    appID = 0
    
    # Props
    name = ""
    version = ""
    description = ""
    
    applicationKey = ""
    privateKey = ""
    
    # One-to-many links    
    ownerID = 0
    
    def generateKeys(self):
        self.privateKey = str(random.randint(10000000, 99999999))
        message = "".join((self.name, self.version, self.description, str(self.created), str(self.ownerID), self.privateKey))
        self.applicationKey = md5.new(message).hexdigest()
        self.setModified()


Application.tabledef = KirbyObject.tabledef(Application, KirbyObject)
Application.keys = ['appID']








class User(KirbyObject):
    """ A User with an account. """
    
    # Key
    userID = 0
    # Props
    userName = ""
    password = ""
    email = ""
    
    curStorage = 0
    maxQuota = 1073741824 # 1 GiB
    overQuota = 10485760 # 10MiB
    
User.tabledef = KirbyObject.tabledef(User, KirbyObject)
User.keys = ['userID']








class Tag(KirbyObject):
    """ A keyword applied to a group of files. """
    
    # Key
    tagID = 0
    
    # Props
    tagName = ""
    
    # One-To-Many Links
    ownerID = 0
            

Tag.tabledef = KirbyObject.tabledef(Tag, KirbyObject)
Tag.keys = ['tagID']





class File(KirbyObject):
    """ A unit of storage. """
    
    # Key
    fileID = 0
    
    # Props
    fileName = ""
    size = 0
    contentType = ""
    
    # One-to-many links
    ownerID = 0
    

File.tabledef = KirbyObject.tabledef(File, KirbyObject)
File.keys = ['fileID']









class ApplicationUser(KirbyObject):
    """ Service contract between app and user """
    
    # Keys (one-to-many links)
    appID = 0
    userID = 0
    # Properties
    unconfirmedToken = ""
    confirmedToken = ""
    
    def __init__(self, app=None):
        if app:
            self.appID = app.appID
    
    def getNewKey(self):
        message = "%10i,%20s,%20s" % (self.appID, str(self.created), str(self.modified))
        return md5.new(message).hexdigest()
        
    def getNewSessionKey(self):
        message = "%10i,%10i,%20s,%20s" % (self.appID, self.userID, str(self.created), str(self.modified))
        digest = sha.new(message).hexdigest()
        # print "Digest: %s" % digest
        return digest
            
    def createOffer(self):
        self.setModified()
        self.unconfirmedToken = self.getNewKey()
    
    def acceptOffer(self, user):
        self.userID = user.userID
        self.setModified()
        self.confirmedToken = self.getNewSessionKey()

    def cancelOffer(self):
        self.confirmedToken = None
        self.setModified()
        
    
ApplicationUser.tabledef = KirbyObject.tabledef(ApplicationUser, KirbyObject)
ApplicationUser.keys = ['unconfirmedToken']








class TagUser(KirbyObject):
    """ Access control for a tag """
    # Keys
    tagID = 0
    userID = 0
    
    # Permission props
    canRead = 1
    canWrite = 0
    canReadACL = 0
    canWriteACL = 0

TagUser.tabledef = KirbyObject.tabledef(TagUser, KirbyObject)
TagUser.keys =['tagID', 'userID']









class FileUser(KirbyObject):
    """ Access control for a file """
    # Keys (one-to-many links)
    fileID = 0
    userID = 0
    
    # Permissions
    canRead = 1
    canWrite = 0
    canReadACL = 0
    canWriteACL = 0
    
    # Token for unauthenticated access
    fileToken = ""
    tokenExpiry = datetime.datetime.today()

    def getNewKey(self, db=None):
        if db: self._db = db
        message = "%10i,%10i,%20s,%20s" % (self.fileID, self.userID, str(self.modified), str(self.tokenExpiry))
        return md5.new(message).hexdigest()
    
    # TODO: Expire these
    def checkout(self, expiry):
        self.tokenExpiry = expiry
        self.setModified()
        self.fileToken = self.getNewKey()
    
    def cancelCheckout(self):
        self.fileToken = ""
        self.setModified()
    
        
FileUser.tabledef = KirbyObject.tabledef(FileUser, KirbyObject)
FileUser.keys = ['fileToken']








class FileTag(KirbyObject):
    """ Tagging of a file """
    # Keys (one-to-many links)
    fileID = 0
    tagID = 0
    
    # Properties
    
FileTag.tabledef = KirbyObject.tabledef(FileTag, KirbyObject)
FileTag.keys = ['fileID', 'tagID']








# Call token requirements


TKN_NONE = 0
TKN_CFM = 1
TKN_APP = 2
TKN_SIG = 4

TKN_STD = TKN_CFM  | TKN_APP | TKN_SIG
TKN_AUTH = TKN_APP | TKN_SIG




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
        






class exposedmethod:
    """ Staticmethod and exposed all in one """
    
    def __init__(self, func):
        self._func = func
        self.exposed = True
        
    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)





# Auth api

class Auth:
    
    tokens = TKN_AUTH
        
    
    
    def GetUnconfirmedToken(req):
        # Generate a new unconfirmed token
        appUser = ApplicationUser.newInstance(
                appID=req.app.appID)
        appUser.createOffer()
        appUser.insert(req.db)
        
        uncfmToken = appUser.unconfirmedToken
     
        # The unconfirmed token is an offer by an
        # application to provide a service.
        # The user authenticates and authorizes 
        # the uncfmToken, accepting of the offer to create 
        # a confirmedToken.
        
        return req.template % {"unconfirmedToken": uncfmToken }
    
    GetUnconfirmedToken = exposedmethod(GetUnconfirmedToken)
    GetUnconfirmedToken.template = "  <unconfirmedtoken>%(unconfirmedToken)s</unconfirmedtoken>\n"
    
    
    
    
    
    
    def GetConfirmedToken(req, unconfirmedToken=None):
        # Find a confirmed token
        appUser = ApplicationUser.select(req.db,
                fields=['unconfirmedToken'],
                vals=[unconfirmedToken], single=True)
        if appUser == ():
            raise OpenomyError(ERR_UNAUTHORIZED)
        cfmToken = appUser.confirmedToken
        
        # The confirmedToken is a contract
        # between a user and an application.
        if not cfmToken:
            raise OpenomyError(ERR_UNAUTHORIZED)
        
        return req.template % {"confirmedToken": cfmToken }
    
    GetConfirmedToken = exposedmethod(GetConfirmedToken)
    GetConfirmedToken.params = {"unconfirmedToken": str}
    GetConfirmedToken.exposed = True
    GetConfirmedToken.template = "  <confirmedtoken>%(confirmedToken)s</confirmedtoken>\n"
    
    
    
    
    
    def AuthorizeUser(req, username=None, password=None):
        # Check the username
        user = User.select(req.db, fields=['userName'], vals=[username], single=True)
        
        # Check username for email, too
        if user == ():
            user = User.select(req.db, fields=['email'], vals=[username], single=True)
        
        # Can't find the user.
        if user == ():
            raise OpenomyError(ERR_BAD_USER)
        
        # Check the password
        if user.password != password:
            raise OpenomyError(ERR_BAD_USER)
        
        # Authorize the application
        appUser = ApplicationUser.newInstance(
                          appID=req.app.appID)
        appUser.createOffer()
        appUser.acceptOffer(user)
        appUser.insert(req.db)
        
        return req.template % {"confirmedToken": appUser.confirmedToken }
        
    AuthorizeUser = exposedmethod(AuthorizeUser)
    AuthorizeUser.params = { "username": str, "password": str }
    AuthorizeUser.exposed = True
    AuthorizeUser.template = GetConfirmedToken.template
    
    
    
    
    
    
    def RegisterUser(req, username=None, password=None, email=None):
        
        # Check the username
        user = User.select(req.db, fields=['userName'], vals=[username], single=True)
        
        # Check username for email, too
        if user == ():
            user = User.select(req.db, fields=['email'], vals=[email], single=True)
    
        if user != ():
            raise OpenomyError(ERR_BAD_USER)
            
        # Register the User
        user = User.newInstance(userName=username, password=password, email=email)
        user.insert(req.db)
        
        # Authorize the Application
        appUser = ApplicationUser.newInstance(
                          appID=req.app.appID)
        appUser.createOffer()
        appUser.acceptOffer(user)
        appUser.insert(req.db)
            
        return req.template % {"confirmedToken": appUser.confirmedToken }
        
        
    RegisterUser = exposedmethod(RegisterUser)
    RegisterUser.params =  { "username": str,
        "password": str, "email": str }
    RegisterUser.exposed = True
    RegisterUser.template = GetConfirmedToken.template
    
    
    
    




# Files api

class Files:
    
    tokens = TKN_STD
    templates = { }
    
    
    
    
    
    def GetFile(req, fileID=None, timeout=1):
        # Check the file permissions
        fileUser = FileUser.select(req.db, 
                                   fields=['fileID', 'userID'], 
                                   vals=["==%i" % fileID, 
                                         "==%i" % req.user.userID], 
                                   single=True) 
        if fileUser == ():
            # Check the tag permissions
            authorized = False
            for fileTag in FileTag.select(req.db, 
                                          fields=['fileID'], 
                                          vals=["==%i" % fileID]):
                                              
                tagUser = TagUser.select(req.db, 
                                         vals=["==%i" % fileTag.tagID, 
                                               "==%i" % req.user.userID], 
                                         single=True)
                                         
                if () != tagUser and tagUser.canRead:
                    authorized = True
                    break
            
            if authorized:
                # Don't calculate the authorization again.
                # Plus, we're checking out the file.
                fileUser = FileUser.newInstance(fileID=fileID,
                             userID=req.user.userID, 
                             canRead=tagUser.canRead,
                             canWrite=tagUser.canWrite, 
                             fullControl=0)
                fileUser.insert(req.db)
                
        elif fileUser.canRead:
            authorized = True
        else:
            authorized = False
    
        # Make sure we passed the permissions check        
        if not authorized:
            raise OpenomyError(ERR_UNAUTHORIZED)
    
        # Checkout a new fileToken
        expiry = datetime.datetime.today() + datetime.timedelta(0, timeout * 60)
        fileUser.checkout(expiry)
        fileUser.update(req.db)
    
        # Retrieve the file object
        file = File.select(req.db, 
                           vals=["==%i" % int(fileID)], 
                           single=True)
        if file == ():
            raise "Server failure."
            
        owner = User.select(req.db, 
                            vals=["==%i" % file.ownerID], 
                            single=True)
        if owner == ():
            owner = req.user
            
        if fileUser.userID == 0 and fileUser.canRead:
            isPublic = True
        else:
            isPublic = False
    
        dateTimeFormat = "%m/%d/%Y %H:%M:%S %p"
        fileInfo = { 
            "fileID": file.fileID,
            "fileName": file.fileName,
            "created": file.created.strftime(dateTimeFormat),
            "modified": file.modified.strftime(dateTimeFormat),
            "contentType": file.contentType,
            "size": file.size,
            "owner": owner.userName,
            "baseurl": "%s/api/download/" % req.environ['openomy.servicepath'],
            "filetoken": fileUser.fileToken,
            "ispublic": isPublic
            }
        
        return req.template % fileInfo
        
    
    GetFile = exposedmethod(GetFile)
    GetFile.params = { "fileID": int, ("timeout",): int }
    GetFile.exposed = True
    GetFile.template = """  <file id="%(fileID)i">
        <filename>%(fileName)s</filename>
        <created>%(created)s</created>
        <modified>%(modified)s</modified>
        <contenttype>%(contentType)s</contenttype>
        <size units="bytes">%(size)i</size>
        <owner>%(owner)s</owner>
        <downloadlink>
          <baseurl>%(baseurl)s</baseurl>
          <filetoken>%(filetoken)s</filetoken>
        </downloadlink>
        <public ispublic="%(ispublic)i" />
      </file>
    """
    
    
    
    
    
    def AddFile(req, fileField=None, tagID=None):
        
        # Check the user quota
        fileSize = fileField.fp.length
        if req.user.maxQuota <= req.user.curStorage:
            raise OpenomyError(ERR_MAX_QUOTA)
            
        if (req.user.overQuota + req.user.maxQuota <
            req.user.curStorage + fileSize):
            raise OpenomyError(ERR_OVER_QUOTA)
            
        if tagID and () == Tag.select(req.db, vals=["==%i" % tagID], single=True):
            raise OpenomyError(ERR_BAD_TAG)
    
        # Adjust the user storage consumption
        req.user.curStorage += fileSize
        req.user.setModified()
        req.user.update(req.db) 
            
        file = File.newInstance(fileName=fileField.filename,
            contentType=fileField.type, size=fileSize,
            ownerID=req.user.userID)
        file.insert(req.db)
        
        # Always generate one for the owner.  Saves time later.
        fileUser = FileUser.newInstance(fileID=file.fileID,
            userID=req.user.userID, fullControl=1, canRead=1,
            canWrite=1)
        fileUser.insert(req.db)
        
        # Store the file contents on disk.
        storedFile = StoredFile.instance(file)
        fileData = fileField.file.read()
        storedFile.setData(fileData)
        
        if tagID:
            fileTag = FileTag.newInstance(fileID=file.fileID, tagID=tagID)
            fileTag.insert(req.db)
        
        return "File uploaded."
    
        #return req.template % file.__dict__
    
    AddFile = exposedmethod(AddFile)
    AddFile.params = { "fileField": None, ("tagID",): int }
    AddFile.exposed = True
    AddFile.template = '  <file id="%(fileID)i">%(fileName)s</file>\n'
    
    
    
    
    
    
    
    def DeleteFile(req, fileID=None):
        # Get the file object
        file = File.select(req.db, 
                           fields=['fileID', 'ownerID'], 
                           vals=["==%i" % fileID, 
                                 "==%i" % req.user.userID], 
                           single=True)
        if file == ():
            raise OpenomyError(ERR_UNAUTHORIZED)
            
        # Adjust the user storage consumption
        req.user.curStorage -= file.size
        req.user.setModified()
        req.user.update(req.db)
    
        # Delete the on-disk file
        storedFile = StoredFile.instance(file)
        storedFile.delete()
        
        # Delete the file record 
        file.delete(req.db)
    
        # Cascade deletion to link tables
        # Delete all the file permissions
        req.db.delete(FileUser.getTableName(), ['fileID'], ["==%i" % fileID])
        
        # Delete all the file tags
        req.db.delete(FileTag.getTableName(), ['fileID'], ["==%i" % fileID])
        
        return "File deleted."
        
    DeleteFile = exposedmethod(DeleteFile)
    DeleteFile.params = { "fileID": int }
    DeleteFile.exposed = True
    
    
    
    
    
    
    
    def ModifyFile(req, fileID=None, fileField=None):
        # Get the user's permissions for the file
        fileUser = FileUser.select(req.db, 
                                   fields=['fileID', 'userID'], 
                                   vals=["==%i" % fileID, 
                                         "==%i" % req.user.userID], 
                                   single=True)    
    
        if fileUser == ():
            # Check tag permissions
            authorized = False
            for fileTag in FileTag.select(req.db, 
                                          fields=['fileID'], 
                                          vals=["==%i" % fileID]):
                                              
                tagUser = TagUser.select(req.db, 
                                         vals=["==%i" % fileTag.tagID, 
                                               "==%i" % req.user.userID], 
                                         single=True)
                if () != tagUser and tagUser.canWrite:
                    authorized = True
                    break
        elif fileUser.canWrite:
            authorized = True
        else:
            authorized = False
        
        
        if not fileUser.canWrite:
            raise OpenomyError(ERR_UNAUTHORIZED)
    
        file = File.select(req.db, vals=["==%i" % fileID], single=True)
        if file == ():
            raise OpenomyError(ERR_UNAUTHORIZED)
    
        # Update the file record        
        file.size = fileField.fp.length
        file.contentType = fileField.type
        file.fileName = fileField.filename
        file.setModified()
        file.update(req.db)
            
        # Store the file contents on disk.
        storedFile = StoredFile.instance(file)
        storedFile.setData(fileField.file.read())
            
        return "File modified."   
        
    ModifyFile = exposedmethod(ModifyFile)
    ModifyFile.params = { "fileID": int, "fileField": None }
    ModifyFile.exposed = True
    
    
    
    
    
    
    
    
    
    def GetAllFiles(req):    
        # Direct user ownership
        fileUsers = FileUser.select(req.db,
                                fields=['userID'], 
                                vals=["==%i" % req.user.userID])
            
        # Convert TagUser and FileUser to File
        files = dict()
        for fileUser in fileUsers:
            file = File.select(req.db, 
                               vals=["==%i" % fileUser.fileID], 
                               single=True)
            if file != ():
                files[file.fileID] = file
            
        # Tag-user files
        for tagUser in TagUser.select(req.db,
                              fields=['userID', 'canRead'],
                              vals=['==%i' % req.user.userID, "==1"]):
            for fileTag in FileTag.select(req.db,
                                          fields=['tagID'],
                                          vals=['==%i' % tagUser.tagID]):
                if fileTag.fileID in files: continue
                file = File.select(req.db,
                                   fields=['fileID'],
                                   vals=['==%i' % fileTag.fileID])
                if file != ():
                    files[file.fileID] = file
        
        # Sort the list by fileID
        fileKeys = files.keys()
        fileKeys.sort()
    
        # Convert to XML
        fitplt = Files.AddFile.template
        fileItems = [ fitplt % files[key].__dict__ for key in fileKeys]
        return req.template % { "fileItems": ''.join(fileItems) }
    
    GetAllFiles = exposedmethod(GetAllFiles)
    GetAllFiles.exposed = True
    GetAllFiles.template = " <files>\n%(fileItems)s </files>\n"
    
    
    
    



# Tags api

class Tags:
    
    tokens = TKN_STD
    templates = { }
    
    
    
    def GetTag(req, tagID=None):
        tag = Tag.select(req.db, 
                         vals=["==%i" % tagID],
                         single=True)
        if tag == ():
            raise OpenomyError(ERR_UNAUTHORIZED)
        
        # Collect the tag users (and check the permissions)
        tagUsers = TagUser.select(req.db, 
                                  fields=['tagID'], 
                                  vals=["==%i" % tagID])
        authorized = False
        users = []
        for tagUser in tagUsers:
            user = User.select(req.db, 
                               vals=["==%i" % tagUser.userID], 
                               single=True)
            if user != ():
                users.append(user)
                if tagUser.canWrite:
                    user.isAdmin = 1
                if (tagUser.userID == req.user.userID
                     and tagUser.canRead):
                    authorized = True
        
        if not authorized:
            raise OpenomyError(ERR_UNAUTHORIZED)
        
        userTemplate = Tags.templates['userItem']
        userItems = [ userTemplate % userItem.__dict__ 
                        for userItem in users ]
        
        fileTemplate = Tags.templates['fileItem']
        fileTags = FileTag.select(req.db, 
                                  fields=['tagID'], 
                                  vals=["==%i" % tagID])
        files = []
        for fileTag in fileTags:
            file = File.select(req.db,
                               vals=["==%i" % fileTag.fileID],
                               single=True)
                               
            if file != ():
                files.append(file)
                file.canRead = 1
                fileUser = FileUser.select(req.db,
                                   fields=['fileID', 'userID'],
                                   vals=["==%i" % fileTag.fileID,
                                         "==%i" % req.user.userID],
                                   single=True)
                if fileUser != () and fileUser.canWrite:
                    file.canWrite = 1
                
        fileItems = [ fileTemplate % file.__dict__ 
                        for file in files ]
        
        dateTimeFormat = "%m/%d/%Y %H:%M:%S %p"
        tagInfo = { 
            "tagID": tagID,
            "tagName": tag.tagName,
            "created": tag.created.strftime(dateTimeFormat),
            "userItems": "".join(userItems),
            "fileItems": "".join(fileItems)
        }
        return req.template % tagInfo
        
    GetTag = exposedmethod(GetTag)
    GetTag.params = { "tagID": int }
    GetTag.exposed = True
    GetTag.template = """  <tag id="%(tagID)i" name="%(tagName)s" created="%(created)s">
        <users>
    %(userItems)s    </users>
        <files>
    %(fileItems)s    </files>
      </tag>
    """
    
    templates["userItem"] = """      <user admin="%(isAdmin)i">%(userName)s</user>
    """
    
    templates["fileItem"] = """      <file id="%(fileID)i" created="%(created)s" readaccess="%(canRead)i" writeaccess="%(canWrite)i">%(fileName)s</file>
    """
    
    
    
    def DeleteTag(req, tagID=None):
        # Make sure the tag exists and the user owns it
        tag = Tag.select(req.db, 
                         fields=['tagID', 'ownerID'],
                         vals=["==%i" % tagID,
                               "==%i" % req.user.userID], 
                         single=True)
    
        if tag == (): raise OpenomyError(ERR_UNAUTHORIZED)
            
        # Delete the tag record
        tag.delete(req.db)
        
        # Delete the TagUser records
        req.db.delete(TagUser.getTableName(), ['tagID'], ["==%i" % tagID])
        
        # Delete the FileTag records
        req.db.delete(FileTag.getTableName(), ['tagID'], ["==%i" % tagID])
    
        # Delete us.
        return "Tag deleted."
        
    DeleteTag = exposedmethod(DeleteTag)
    DeleteTag.params = { "tagID": int }
    DeleteTag.exposed = True
    
    
    
    
    
    
    
    def CreateTag(req, tagName=None):
        # Check for a tag by this name already in this user's namespace
        tagsWithName = Tag.select(req.db, fields=['tagName'], vals=[tagName])
                                  
        for tag in tagsWithName:
            tagUser = TagUser.select(req.db, 
                                     vals=["==%i" % tag.tagID, 
                                           "==%i" % req.user.userID], 
                                     single=True)
            if tagUser != ():
                raise OpenomyError(ERR_BAD_TAG)
            
        # Create the new tag
        tag = Tag.newInstance(tagName=tagName, ownerID=req.user.userID)
        tag.insert(req.db)
        
        # Add the owner permissions
        tagUser = TagUser.newInstance(tagID = tag.tagID,
                        userID=req.user.userID,
                        canRead=1, canWrite=1)
        tagUser.insert(req.db)
        
        return req.template % tag.__dict__
    
        
    CreateTag = exposedmethod(CreateTag)
    CreateTag.params = { "tagName": str }
    CreateTag.exposed = True
    CreateTag.template = '  <tag id="%(tagID)i">%(tagName)s</tag>\n'
    
    
    
    
    
    
    def AddFileToTag(req, fileID=None, tagID=None):
        file = File.select(req.db, 
                           fields=['fileID', 'ownerID'], 
                           vals=["==%i" % fileID, 
                                 "==%i" % req.user.userID], 
                           single=True)
    
        tag = Tag.select(req.db, vals=["==%i" % tagID], single=True)
    
        if file == () or tag == ():
            raise OpenomyError(ERR_UNAUTHORIZED)
        
        # Check the tag permissions
        if not tag.ownerID == req.user.userID:
            # Check for a tagUser
            tagUser = TagUser.select(req.db, 
                                     vals=["==%i" % tagID, 
                                           "==%i" % req.user.userID], 
                                     single=True)
            if tagUser == () or not tagUser.canWrite:
                raise OpenomyError(ERR_UNAUTHORIZED)
        
        # Check to see if the file is tagged already
        tagFile = FileTag.select(req.db, 
                                 vals=["==%i" % fileID, 
                                       "==%i" % tagID], 
                                 single=True)
        if tagFile != ():
                raise OpenomyError(ERR_BAD_FILETAG)
        
        # Create the tag
        tagFile = FileTag.newInstance(tagID=tagID, fileID=fileID)
        tagFile.insert(req.db)
                
        return "File added to tag."
    
    AddFileToTag = exposedmethod(AddFileToTag)
    AddFileToTag.params = { "fileID": int, "tagID": int }
    AddFileToTag.exposed = True
    
    
    
    
    
    
    def DeleteFileFromTag(req, fileID=None, tagID=None):
        # Load the file and tag data
        file = File.select(req.db, 
                           vals=["==%i" % fileID], 
                           single=True)
    
        tag = Tag.select(req.db, 
                         vals=["==%i" % tagID], 
                         single=True)
        
        # Make sure the file and tag both exist
        if () in (file, tag):
            raise OpenomyError(ERR_UNAUTHORIZED)
            
        # If the user is not the owner, see if they can edit the tag
        if tag.ownerID != req.user.userID:
            tagUser = TagUser.select(req.db, 
                                     vals=["==%i" % tagID, 
                                           "==%i" % req.user.userID], 
                                     single=True)
    
            if tagUser == () or not tagUser.canWrite:
                raise OpenomyError(ERR_UNAUTHORIZED)
        
        # Make sure the file actually belongs to the tag
        fileTag = FileTag.select(req.db, 
                                 vals=["==%i" % fileID, 
                                       "==%i" % tagID], 
                                 single=True)
        if fileTag == ():
            raise OpenomyError(ERR_BAD_FILETAG)
        
        # Finally remove the tag    
        fileTag.delete(req.db)
        return "File removed from tag."
    
    DeleteFileFromTag = exposedmethod(DeleteFileFromTag)
    DeleteFileFromTag.params = { "tagID": int, "fileID": int }
    DeleteFileFromTag.exposed = True
    
    
    
    
    
    
    
    def GetAllTags(req):
        titplt = Tags.CreateTag.template
        
        # Collect all the tag names
        tagItems = []
        for tagUser in TagUser.select(req.db, fields=['userID'],
            vals=["==%i" % req.user.userID]):
            tag = Tag.select(req.db, vals=["==%i" % tagUser.tagID], single=True)
            if tag != ():
                tagItems.append( titplt % tag.__dict__ )
        
        allTags = { "tagItems": ''.join(tagItems) }
        return req.template % allTags
    
    GetAllTags = exposedmethod(GetAllTags)
    GetAllTags.exposed = True
    GetAllTags.template = "  <tags>\n%(tagItems)s  </tags>\n"
    
    






# Debug api

class Debug:
    
    tokens = TKN_NONE 
    
    templates = { }
        
    
    
    
    def CreateApplication(req, name=None, version=None, description=None, ownerID=None):
    
        app = Application.newInstance(name=name, version=version, description=description, ownerID=ownerID)
        app.generateKeys()
        app.insert(req.db)
        
        return req.template % app.__dict__
    
    
    CreateApplication = exposedmethod(CreateApplication)
    CreateApplication.params = { "name": str, "version": str, "description": str, "ownerID": int }
    CreateApplication.template = """  <application id="%(appID)i">
        <applicationKey>%(applicationKey)s</applicationKey>
        <privateKey>%(privateKey)s</privateKey>
      </application>""" + "\n"
    
    
    
    
    def ListMethods(req):
        mitplt = Debug.templates['methodItem']
        
        # Collect all the method names
        methodItems = list()
        for segment in Auth, Files, Tags, Debug:
            s = [ mitplt % (segment.__name__ + "." + func)
                    for func in segment.__dict__ 
                    if callable(getattr(segment, func)) ]
            methodItems.extend(s)
        
        return req.template %  { "methodItems": ''.join(methodItems) }
    
    ListMethods = exposedmethod(ListMethods)
    ListMethods.exposed = True
    ListMethods.params = {}
    ListMethods.template = """  <methods>
    %(methodItems)s  </methods>""" + "\n"
    
    templates["methodItem"] = "    <method>%s</method>\n"
    
    
    
    
    
    def Shutdown(req):
        pid = os.getpid()
        if os.name == "posix":
            import signal
            os.kill(pid, signal.SIGTERM)
        elif os.name == "nt":
            import win32api
            handle = win32api.OpenProcess(1, 0, pid)
            return (0 != win32api.TerminateProcess(handle, 0))
    
    Shutdown = exposedmethod(Shutdown)
    Shutdown.exposed = True
    
    
    
    
    
    
    def GetRecord(req, table=None, keyval=None):
        if not globals()[table]:
            raise OpenomyError()
        table = globals()[table]
        
        record = table.select(req.db, vals=["==" + keyval], single=True)
        tabledef = table.tabledef
        if callable(tabledef): tabledef = tabledef()
        
        fieldTemplate = Debug.templates['fieldItem']
        fieldItems = list()
        for field in tabledef:
            fieldName = field.split(":")[0]
            fieldValue = getattr(record, fieldName, None)
            fieldItems.append(fieldTemplate % locals())
        
        return req.template % { "fieldItems": "".join(fieldItems),
            "tableName": table.getTableName(), "recno": record.recno }
    
    GetRecord = exposedmethod(GetRecord)
    GetRecord.params = { "table": str, "keyval": str }
    GetRecord.exposed = True
    GetRecord.template = """  <record table="%(tableName)s" recno="%(recno)i">
        <fields>
    %(fieldItems)s    </fields>
      </record>""" + "\n"
    
    
    
    templates["fieldItem"] = """      <field name="%(fieldName)s">%(fieldValue)s</field>""" + "\n"
    
    
    
    
    
    
    def GetTable(req, table=None):
        # Get the table definition
        if not globals()[table]:
            raise OpenomyError()
        table = globals()[table]
        tabledef = table.tabledef
        if callable(tabledef): tabledef = tabledef()
        
        # Generate the response
        fieldTemplate = Debug.templates['fieldItem']
        fieldItems = list()
        for field in tabledef:
            fieldName, fieldValue = field.split(":")
            fieldItems.append(fieldTemplate % locals())
        
        return req.template % { "fieldItems": "".join(fieldItems),
                                "tableName": table.getTableName() }
    
    GetTable = exposedmethod(GetTable)
    GetTable.params = { "table": str }
    GetTable.exposed = True
    GetTable.template = """  <table name="%(tableName)s">
        <fields>
    %(fieldItems)s    </fields>
      </table>""" + "\n"
    
    
    
    
    
    
    
    def Reinitialize(req):
        """ Reinitialize the database. """
        for klass in (User, Tag, File, Application, ObjectID,
                        ApplicationUser, FileUser, TagUser, FileTag):
            # Drop the table
            klass.dropTable(req.db)
            # Recreate the table
            klass.createTable(req.db)
            # Initialize the records
            klass.initTable(req.db)
        
        
        if not os.path.exists(StoredFile.PATH):
            os.makedirs(StoredFile.PATH)
        
        return "Server reinitialized."
    
    
    Reinitialize = exposedmethod(Reinitialize)
    Reinitialize.exposed = True
    
    





class REST:
        
    params = { } 
    exposed = True
    
     
    
    class SimpleObject:
        def __init__(self, **attrs):
            for (attr, val) in attrs.items():
                setattr(self, attr, val)
    
    def __init__(self, **objects):
        self._root = REST.SimpleObject(**objects)
        
        # Collect the method info
        tocollect = ('params', 'template', 'tokens')        
        collected = dict()
        self._methods = dict()
        for klassName, klass in objects.items():
            klassCollected = dict(collected)
            klassCollected.update(dict( [ (key, getattr(klass, key))
                  for key in tocollect if hasattr(klass, key) ] ))
            
            for methName, method in klass.__dict__.items():
                if callable(method) and getattr(method, 'exposed', False):
                    methCollected = dict(klassCollected)
                    methCollected.update(dict( [ (key, getattr(method, key))
                          for key in tocollect if hasattr(method, key) ] ))
                    methCollected['method'] = method
                    fullName = "%s.%s" % (klassName, methName)
                    self._methods[fullName] = methCollected
                
    
    
    def __call__(self, req):
        """ Lookup and execute the method. """
        
        try:
            # Check the method call
            self.filter(req)
                   
            # Collect the arguments
            result = req.method(req, **req.callParams)
            if str(result) == result:
                req.environ['wsgi.response'].write(result)
    
        except OpenomyError, f:
            req.environ['wsgi.response'].status_code = 400
            req.environ['wsgi.response'].failure = f
            return self._failure(req)
            
        return self._success(req)
    
    
    
    
    
    
    
    def filter(self, req):
        """ Make sure we have a semantically correct
            Openomy call. """
        
        # Check the method name.
        fv = req.params
        methName = fv.get('method', None)
        if methName not in self._methods:
            raise OpenomyError(ERR_BAD_METHOD)
        
        # Traverse to find the method
        methInfo = self._methods[methName]
        req.__dict__.update(methInfo)
        if 'params' in methInfo:
            req.methodParams = methInfo['params']
        else:
            req.methodParams = {}
        
        # Check the tokens and keys and signature
        reqTokens = req.tokens
        
        # AppToken
        if reqTokens & TKN_APP:
            if 'applicationKey' not in fv:
                # Missing application key
                raise OpenomyError(ERR_MISSING_ARG)
            req.app = Application.select(req.db,
                fields=['applicationKey'],
                vals= [fv['applicationKey']], single=True)
            if req.app == ():
                raise OpenomyError(ERR_BAD_APP_KEY)
        
    
        # CfmToken
        if reqTokens & TKN_CFM:
            if 'confirmedToken' not in fv:
                raise OpenomyError()
            req.appUser = ApplicationUser.select(req.db,
                fields=['confirmedToken'],
                vals=[fv['confirmedToken']], single=True)
            if req.appUser == ():
                raise OpenomyError(ERR_BAD_TOKEN)
            if req.appUser.appID != req.app.appID:
                raise OpenomyError(ERR_UNAUTHORIZED)
            req.user = User.select(req.db,
                vals=["==%i" % req.appUser.userID], single=True)
            if req.user == ():
                raise OpenomyError(ERR_BAD_USER)
                
        # Signature
        if reqTokens & TKN_SIG:
            if 'signature' not in fv:
                raise OpenomyError(ERR_MISSING_ARG)
    
            # Create a comparison signature
            keylist = req.methodParams.keys()
            # print "Base Parms: %s" % keylist
            keylist.append("method")
            if reqTokens & TKN_APP:
                keylist.append('applicationKey')
            if reqTokens & TKN_CFM:
                keylist.append('confirmedToken')
    
            # @@ Don't hash the file contents.
            if 'fileField' in keylist:
                keylist.remove('fileField')
            
            for nKey in range(len(keylist)):
                key = keylist[nKey]
                if tuple(key) == key:
                    keylist[nKey] = key[0]
            
            # print "Parms: %s" % keylist
    
            keylist.sort()
            sigdat = "".join([ "%s=%s" % (str(k), str(fv.get(k)))
                               for k in keylist if k in fv ])
            
            sigdat += req.app.privateKey
            # print "Signature data: %s" % sigdat
            sig = md5.new(sigdat).hexdigest()
        
            # Check the signature.
            if fv['signature'] != sig:
                raise OpenomyError(ERR_BAD_SIG)
    
        # Check and collect the parameters
        req.callParams = dict()
        for pname in req.methodParams:
            ptype = req.methodParams[pname]
            
            if (tuple(pname) != pname and 
                pname not in fv):
                # Missing required parameter
                raise OpenomyError(ERR_MISSING_ARG)
            
            # Fix the type
            if tuple(pname) == pname: 
                pname = pname[0]
                
            if pname in fv:
                val = fv[pname]
                if ptype is not None:
                    try:
                        val = ptype(val)
                    except TypeError:
                        raise OpenomyError(ERR_BAD_ARG)
                        
                req.callParams[pname] = val
                
        # Successfully passed the filter.
        return None
    
    
    
    
    
    
    def _success(self, req):
        """ Wrap the body in a success tag. """
        message = ''.join(req.environ['wsgi.response'].content)
        if not message.endswith("\n"): message += "\n"
        if not message.startswith(" "):
            message = "  " + message
        body = "<success>\n%s</success>" % message
        req.environ['wsgi.response'].content = [
                '<?xml version="1.0" encoding="UTF-8"?>\n', 
                body]
        
    
    
    
    
        
    def _failure(self, req):
        """ Wrap the body in a failure tag. """
        message = req.environ['wsgi.response'].failure.message
        if not message.endswith("\n"): message += "\n"
        if not message.startswith(" "):
            message = "  " + message
        body = "<error>\n%s</error>" % message
        req.environ['wsgi.response'].content = ['<?xml version="1.0" encoding="UTF-8"?>\n', body]
    
    
    




class Download:
              
    
    
    def __call__(self, req):
        try:
            # Call the method.
            self.filter(req)
            req.environ['wsgi.response'].headers['Content-Type'] = req.file.contentType
            req.environ['wsgi.response'].write(req.storedFile.getData())
            
        except OpenomyError, f:
            req.environ['wsgi.response'].status_code = 400
            req.environ['wsgi.response'].failure = f
            return self._failure(req)
    
    
    
    
    def filter(self, req):
        # Check the file token
        fv = req.params
        fileToken = req.fileToken = fv.get('fileToken', None)
    
        req.fileUser = FileUser.select(req.db, 
                                       fields=['fileToken'], 
                                       vals=[fileToken], 
                                       single=True)
                                       
        if req.fileUser == ():
            raise OpenomyError(ERR_UNAUTHORIZED)
            
        req.file = File.select(req.db, 
                               vals=["==%i" % req.fileUser.fileID], 
                               single=True)
        if not req.file:
            raise OpenomyError(ERR_UNAUTHORIZED)
            
        req.storedFile = StoredFile.instance(req.file)
        
        
    
    
        
    def _failure(self, req):
        """ Wrap the body in a failure tag. """
        message = req.environ['wsgi.response'].failure.message
        if not message.endswith("\n"): message += "\n"
        if not message.startswith(" "):
            message = "  " + message
        body = "<error>\n%s</error>" % message
        req.environ['wsgi.response'].content = ['<?xml version="1.0" encoding="UTF-8"?>\n', body]
    
    
    
    
    



MODE_TEST = "testing"
MODE_PRODUCTION = "production"

class Service:
    """ Works as either a self-contained WSGI server
        or a WSGI application. """
        
    
    
    
    def __init__(self, application=None, mode=MODE_TEST):
        # Create the root dispatcher
        self.dispatcher = dp = application or URLMap()
        
        # Create and bind the REST applications
        restApi = {
            "Auth": Auth,
            "Tags": Tags,
            "Files": Files
            }
            
        if mode == MODE_TEST:
            restApi['Debug'] = Debug
            
        dp[None, '/api/rest'] = REST(**restApi)
    
        # Create and bind the download application
        dp[None, '/api/download'] = Download()
        
        wsgi_app = HTTPExceptionHandler(self)
    
        if mode == MODE_PRODUCTION:
            wsgi_app = ErrorMiddleware(wsgi_app)
        else:
            wsgi_app = ErrorMiddleware(wsgi_app, debug=True)
            wsgi_app = TransLogger(wsgi_app)
    
        # Us, all wrapped up.
        self.wsgi_app = wsgi_app
    
    
    
    
        
    def __call__(self, environ, start_response):
        """ Dispatch to the applications """
        req = Request(environ)
        app = self.dispatcher[environ['PATH_INFO']]
        
        app(req)
        
        response = environ['wsgi.response']
        status, headers, output = response.wsgi_response()
    
        start_response(status, headers)
        return output
    
    
        
    def serve(self, host='', port=80):
        print "Starting Openomy API server..."
        from paste import httpserver
        httpserver.serve(self.wsgi_app, host=host, port=port)
    
    



def fixReadLine(obj):
    
    def readline(lines=None):
        return obj.oldReadline()
    
    obj.oldReadline = obj.readline
    obj.readline = readline
    return readline


class Request(WSGIRequest):

  def __init__(self, environ):
    WSGIRequest.__init__(self, environ)
    
    # Fix-up the readline to accept, but ignore
    # the max-length argument
    fixReadLine(self.environ['wsgi.input'])

    # Setup some extra request values    
    self.db = KirbyBase('server')
    environ['wsgi.response'] = WSGIResponse(mimetype="text/xml")

    # Setup the request root
    server = self.environ['HTTP_HOST']
    rootpath = ""
    if 'OPENOMY_APP_ROOT' in self.environ:
        rootpath = self.environ['OPENOMY_APP_ROOT']
        # Decapitate the path as necessary
        if self.environ['PATH_INFO'].startswith(rootpath):
            self.environ['PATH_INFO'] = self.environ['PATH_INFO'][len(rootpath):]
    self.environ['openomy.servicepath'] = "http://%s%s" % (server, rootpath)





_theApp = None
def getApp(mode=MODE_TEST):
    """ Return the global Openomy application service. """
    global _theApp
    if _theApp is None:
        _theApp = Service(mode=mode)
    return _theApp
    

# For mod_python
def app(environ, start_response):
    """ Handle a single response. """
    # Cache the service initialization
    theApp = getApp(MODE_PRODUCTION)
    return theApp(environ, start_response)



# For command line startup
if __name__ == "__main__":
    # Serve until KILL-ed.
    getApp().serve("localhost", 9009)




