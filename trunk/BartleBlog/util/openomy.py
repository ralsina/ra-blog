# -*- coding: utf-8 -*-

import urllib2,md5
from StringIO import StringIO
import elementtree.ElementTree as tree
import BartleBlog.backend.config as config

appkey='1e31cb69be8d30070f7607b4f23d4f95'
secret='39578658'


baseurl='http://www.openomy.com/api/rest/?'

errors={0:['Invalid token','The token (either unconfirmed or confirmed) was not valid.'],
        1:['Invalid signature','The MD5 based signature did not match what Openomy produced.'],
        2:['Permissions','The application does not have enough permissions to perform the requested call.'],
        3:['Null Reference','One or more of the arguments was null. You\'re probably missing an argument (maybe a token or key?).'],
        4:['General','A general, undescribed, error occured.'],
        5:['Tag Name Not Valid','The name of the tag you are describing is not valid. Perhaps forbidden characters or already used?'],
        6:['User Not Found','The user you are requesting was not found.'],
        7:['File Too Large','The file you are trying to upload was too large based on the user\'s quota.'],
        8:['Out Of Storage','The user is out of storage space and the requested call could not be completed.'],
        9:['InvalidApplicationKey','The applicationKey you passed was invalid.'],
        10:['UnknownMethod',"The method you passed was unknown (or you didn't pass a method)."],
        11:['No token configured','There is no token configured to access openomy.com, please configure the Openomy tool'],
        12:['No such tag','There is no tag with that name in openomy.com'],
        13:['No such file','There is no file with that name in openomy.com'],
        18:['Authentication error','Username not found']
}


class OpenomyError(Exception):
    def __init__(self,code,xml):
        print "Openomy error: ",code
        print
        print xml
        self.error=errors[code]

                
                
class File:
    def __init__(self,tree):
        self.filename=tree.find('file').find('filename').text
        self.created=tree.find('file').find('created').text
        self.modified=tree.find('file').find('modified').text
        self.contenttype=tree.find('file').find('contenttype').text
        self.size=tree.find('file').find('size').text
        self.owner=tree.find('file').find('owner').text
        self.public=tree.find('file').find('public').attrib['ispublic']=='1'
        self.url=tree.find('file').find('public').text
                
class Tag:
    def __init__(self,element):
        self.name=element.text
        self.id=element.attrib['id']
        self.users=None
        self.files=None

class Openomy:
    
    def __init__(self,notoken=False):
        self.tags={}
        self.files={}
        if not notoken:
            self.tok=config.getValue('openomy','token')
            if not self.tok:
                raise OpenomyError(11)
        
    def Files_GetFile(self,fname,nocache=False):
        if not self.files.has_key(id) or nocache:
            self.Files_GetAllFiles(nocache)
            try:
                u=self.createUrl('Files.GetFile',tok=self.tok,fileID=self.files[fname])
            except KeyError:
                raise OpenomyError(13)
            resp=self.getResponse(u)
            f=File(resp)
        else:
            f=self.files[id]
        return f
            
    def Files_GetAllFiles(self,nocache=False):
        if nocache or not self.files:
            u=self.createUrl('Files.GetAllFiles',tok=self.tok)
            resp=self.getResponse(u)
            fs=[ (x.attrib['id'],x.text) for x in resp.find('files').findall('file') ]
            for f in fs:
                self.files[f[1]]=f[0]
        return self.files
            
        
    def Tags_GetTag(self,name,nocache=False):
        ts=self.Tags_GetAllTags(nocache)
        try:
            tag=ts[name]
        except:
            raise OpenomyError(12)
        if nocache or (tag.users==None or tag.files==None):
            # Need to fetch data
            u=self.createUrl('Tags.GetTag',tok=self.tok,tagID=tag.id)
            resp=self.getResponse(u)
            tag.users=[ x.text for x in resp.find('tag').find('users').findall('user') ]
            tag.files=[ x.text for x in resp.find('tag').find('files').findall('file') ]
        return tag
        
    def Tags_GetAllTags(self,nocache=False):
        if nocache:
            self.tags={}
        if not self.tags:
            u=self.createUrl('Tags.GetAllTags',tok=self.tok)
            resp=self.getResponse(u)
            for e in resp.find('tags').findall('tag'):
                t=Tag(e)
                self.tags[t.name]=t
        return self.tags
        
    def Auth_AuthorizeUser(self,username,password):
        u=self.createUrl('Auth.AuthorizeUser',username=username,password=password)
        print u
        resp=self.getResponse(u)
        return resp.find('confirmedtoken').text
        
    def createUrl(self,method,tok=None,**params):
    
        params['method']=method
        params['applicationKey']=appkey
        
        if method=='Auth.AuthorizeUser':
                pass
        elif method=='Auth.GetConfirmedToken':
                params['unconfirmedToken']=self.tok
        else:
                params['confirmedToken']=self.tok
        k=params.keys()
        k.sort()
        url=baseurl+'&'.join([ '%s=%s'%(key,params[key]) for key in k])
        
        sig=''.join(['%s=%s'%(key,params[key]) for key in k])+secret
        url=url+'&signature=%s'%md5.md5(sig).hexdigest()
        return url
    
    def getResponse(self,url):
        data=urllib2.urlopen(url).read()
        f=StringIO(data)
        
        t=tree.parse(f)
        
        r=t.getroot()
        if r.tag=='error':
                raise OpenomyError(int(r.attrib['code']),data)
        return r
