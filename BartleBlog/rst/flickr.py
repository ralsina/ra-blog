# -*- coding: utf-8 -*-

import docutils.core
import docutils.parsers.rst
import BartleBlog.util.flickrapi as flickrapi
import sys

flickrAPIKey='a4b67aa4c75657b2db3ebc2f2f43c136'
fapi=flickrapi.FlickrAPI(flickrAPIKey,'ab116226d50899a7')


def flickrset( name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine ):
    """
    A directive that produces a table with all thepictures in a flickr set in HTML.

    The syntax is this::

        .. flickrset:: setname

    Where setname is the name of the set in flickr.
    """
    
    
def htmlforphotoid(id):
    token = fapi.getToken(browser="firefox")
    
    photo = fapi.photos_getInfo(api_key=flickrAPIKey,auth_token=token,photo_id=id) 
    owner=photo.photo[0].owner[0]
    secret=photo.photo[0]['secret']
    
    try:
      realname=owner['realname']
    except:
      realname=owner['username']
      
    photosurl=photo.photo[0].urls[0].url[0].elementText
    fname=photo.photo[0].title[0].elementText
    
    rsp = fapi.photos_getInfo(api_key=flickrAPIKey,auth_token=token,photo_id=id,secret=secret)

    farm=rsp.photo[0]['farm']
    server=rsp.photo[0]['server']

    url= 'http://www.flickr.com/photos/%s/%s'%(owner,id)
    t_url='http://farm%s.static.flickr.com/%s/%s_%s_%s.jpg'%(
            farm,server,id,secret,'m')

    html='<div class="center"><a href="%s"><img src="%s" class="flickr" alt="%s"></a><div class="footerbox">%s by <a href="%s">%s</a></div></div>'%(url,t_url,fname,fname,photosurl,realname)
    return html

def flickr( name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine ):
    """
    A directive that produces a nicely styled image from flickr in HTML.

    The syntax is this::

        .. flickr:: title
           :user: username 
           :id: NSID

    Where title is the title you used in flickr, and the optional username argument is
    what user owns the picture (if it's not you)
    """

    print arguments,options

    token = fapi.getToken(browser="firefox")
    fname=' '.join(arguments)
    if 'id' in options:
      id=options['id'] 
    else: 
      if 'user' in options:
        #First get the userid
        try:
          username=options['user']
          rsp = fapi.people_findByUsername(api_key=flickrAPIKey,auth_token=token,username=username)
          user=rsp.user[0]['nsid']
        except AttributeError:
          error = state_machine.reporter.error( "Can't find user called %s in Flickr"%username,
                      docutils.nodes.literal_block(block_text, block_text), line=lineno )
          return [error]
        
      else:
        user='me'
      rsp = fapi.photos_search(api_key=flickrAPIKey,auth_token=token,user_id=user,text=fname)

      # Get the secret and ID of the photo
      try:
          photo=rsp.photos[0].photo[0]
          id=photo['id']
      except AttributeError:
          error = state_machine.reporter.error( "Can't find image called %s in Flickr"% fname,
                      docutils.nodes.literal_block(block_text, block_text), line=lineno )
          return [error]

    html=htmlforphotoid(id)

    raw = docutils.nodes.raw('',html, format = 'html')
    return [raw]

flickr.arguments = (1,2,1)
flickr.options = {'name' : docutils.parsers.rst.directives.unchanged, 
                  'user' : docutils.parsers.rst.directives.unchanged,
                  'id' : docutils.parsers.rst.directives.unchanged,
                 }
flickr.content = 1

# Simply importing this module will make the directive available.
docutils.parsers.rst.directives.register_directive( 'flickr', flickr )

if __name__ == "__main__":
    import docutils.core
    docutils.core.publish_cmdline(writer_name='html')
