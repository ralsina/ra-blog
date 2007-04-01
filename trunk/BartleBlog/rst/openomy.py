# -*- coding: utf-8 -*-

import docutils.core
import docutils.parsers.rst
import os,urllib2,md5,sys
from StringIO import StringIO
import elementtree.ElementTree as tree

import BartleBlog.backend.config as config

appkey='1e31cb69be8d30070f7607b4f23d4f95'
secret='39578658'
baseurl='http://www.openomy.com/api/rest/?'

errors=[
        [0,'Invalid token','The token (either unconfirmed or confirmed) was not valid.'],
        [1,'Invalid signature','The MD5 based signature did not match what Openomy produced.'],
        [2,'Permissions','The application does not have enough permissions to perform the requested call.'],
        [3,'Null Reference','One or more of the arguments was null. You\'re probably missing an argument (maybe a token or key?).'],
        [4,'General','A general, undescribed, error occured.'],
        [5,'Tag Name Not Valid','The name of the tag you are describing is not valid. Perhaps forbidden characters or already used?'],
        [6,'User Not Found','The user you are requesting was not found.'],
        [7,'File Too Large','The file you are trying to upload was too large based on the user\'s quota.'],
        [8,'Out Of Storage','The user is out of storage space and the requested call could not be completed.'],
        [9,'InvalidApplicationKey','The applicationKey you passed was invalid.'],
        [10,'UnknownMethod',"The method you passed was unknown (or you didn't pass a method)."]
]

class OpenomyError(Exception):
        def __init__(self,code):
                self.error=errors[code]

def createUrl(method,tok=None,**params):

        params['method']=method
        params['applicationKey']=appkey

        if method=='Auth.AuthorizeUser':
                pass
        elif method=='Auth.GetConfirmedToken':
                params['unconfirmedToken']=tok
        else:
                params['confirmedToken']=tok
        k=params.keys()
        k.sort()
        print params
        url=baseurl+'&'.join([ '%s=%s'%(key,params[key]) for key in k])

        sig=''.join(['%s=%s'%(key,params[key]) for key in k])+secret
        url=url+'&signature=%s'%md5.md5(sig).hexdigest()
        return url

def getResponse(url):
        print  "Fetching: ",url
        data=urllib2.urlopen(url).read()
        f=StringIO(data)
        print data
        t=tree.parse(f)

        r=t.getroot()
        if r.tag=='error':
                raise OpenomyError(int(r.attrib['code']))
        return r

def directive_openomy_tag (name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine ):
    """
    A directive that produces a table with links to all public files 
    stored in openomy.com and tagged with a given tag.

    The syntax is this::

    .. openomy_tag:: tagname

    Where tagname is the one you use in openomy.com.
    """
    tname=arguments[0]
    
    try:
    
        tok=config.getValue('openomy','token')
        if not tok:
            error = state_machine.reporter.error( "Please Configure the Openomy Module Before using the openomy directive.",docutils.nodes.literal_block(block_text, block_text), line=lineno )
            return [error]

        u=createUrl('Tags.GetAllTags',tok=tok)
        resp=getResponse(u)

        html=''
        
        for t in resp.find('tags').findall('tag'):
            if t.text==tname:
                u=createUrl('Tags.GetTag',tok=tok,tagID=t.attrib['id'])
                resp=getResponse(u)
                fids=[ f.attrib['id'] for f in resp.find('tag').find('files').findall('file')]
                print fids
                for fid in fids:
                    u=createUrl('Files.GetFile',tok=tok,fileID=fid)
                    resp=getResponse(u)
                    f=resp.find('file')
                    fname=f.find('filename').text
                    pub=f.find('public')
                    if pub.attrib['ispublic']=='1':
                        html+='<a href="%s">%s</a>'%(pub.text,fname)
                    else:
                        error = state_machine.reporter.error( "The file %s is not marked as public."% fname,
                        docutils.nodes.literal_block(block_text, block_text), line=lineno )
                        return [error]
                break

        raw = docutils.nodes.raw('',html, format = 'html')
        return [raw]
    
    except OpenomyError, e:
        error = state_machine.reporter.error( e.error[2],
        docutils.nodes.literal_block(block_text, block_text), line=lineno )
        return [error]

directive_openomy_tag.arguments = (1,0,0)
directive_openomy_tag.options = {'name' : docutils.parsers.rst.directives.unchanged }
directive_openomy_tag.content = 1

# Simply importing this module will make the directive available.
docutils.parsers.rst.directives.register_directive( 'openomy_tag', directive_openomy_tag )

        
def directive_openomy( name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine ):
    """
    A directive that produces a link to a file stored in openomy.com

    The syntax is this::

    .. openomy:: filename

    Where filename is the one you uploaded to openomy.com.
    """

    fname=arguments[0]
    
    try:
    
        tok=config.getValue('openomy','token')
        if not tok:
            error = state_machine.reporter.error( "Please Configure the Openomy Module Before using the openomy directive.",docutils.nodes.literal_block(block_text, block_text), line=lineno )
            return [error]

        u=createUrl('Files.GetAllFiles',tok=tok)
        resp=getResponse(u)
        for f in resp.find('files').findall('file'):
            if f.text==fname:            
                u=createUrl('Files.GetFile',tok=tok,fileID=f.attrib['id'])
                resp=getResponse(u)
                f=resp.find('file')
                pub=f.find('public')
                if pub.attrib['ispublic']=='1':
                    html='<a href="%s">%s</a>'%(pub.text,fname)
                else:
                    error = state_machine.reporter.error( "The file %s is not marked as public."% fname,
                    docutils.nodes.literal_block(block_text, block_text), line=lineno )
                    return [error]
        
        raw = docutils.nodes.raw('',html, format = 'html')
        return [raw]
    
    except OpenomyError, e:
        error = state_machine.reporter.error( e.error[2],
        docutils.nodes.literal_block(block_text, block_text), line=lineno )
        return [error]

directive_openomy.arguments = (1,0,0)
directive_openomy.options = {'name' : docutils.parsers.rst.directives.unchanged }
directive_openomy.content = 1

# Simply importing this module will make the directive available.
docutils.parsers.rst.directives.register_directive( 'openomy', directive_openomy )

if __name__ == "__main__":
  import docutils.core
  docutils.core.publish_cmdline(writer_name='html')
