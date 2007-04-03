# -*- coding: utf-8 -*-

import docutils.core
import docutils.parsers.rst

import BartleBlog.util.flickrapi as flickrapi

def flickr( name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine ):
    """
    A directive that produces a nicely styled image from flickr in HTML.

    The syntax is this::

    .. flickr:: title

    Where title is the title you used in flickr.
    """

    flickrAPIKey='a4b67aa4c75657b2db3ebc2f2f43c136'

    fapi=flickrapi.FlickrAPI(flickrAPIKey,'ab116226d50899a7')
    token = fapi.getToken(browser="firefox")
    fname=arguments[0]
    rsp = fapi.photos_search(api_key=flickrAPIKey,auth_token=token,user_id='me',text=fname)

    # Get the secret and ID of the photo

    if len(rsp.photos[0].photo)==0:
        error = state_machine.reporter.error( "Can't find image called %s in Flickr"% fname,
                    docutils.nodes.literal_block(block_text, block_text), line=lineno )
        return [error]

    id=rsp.photos[0].photo[0]['id']
    secret=rsp.photos[0].photo[0]['secret']
    owner=rsp.photos[0].photo[0]['owner']
    print rsp.photos[0].photo[0]['title']

    rsp = fapi.photos_getInfo(api_key=flickrAPIKey,auth_token=token,photo_id=id,secret=secret)

    farm=rsp.photo[0]['farm']
    server=rsp.photo[0]['server']


    url= 'http://www.flickr.com/photos/%s/%s'%(owner,id)
    t_url='http://farm%s.static.flickr.com/%s/%s_%s_%s.jpg'%(
            farm,server,id,secret,'m')

    html='<a href="%s"><img src="%s" class="flickr"></a>'%(url,t_url)

    raw = docutils.nodes.raw('',html, format = 'html')
    return [raw]

flickr.arguments = (1,0,0)
flickr.options = {'name' : docutils.parsers.rst.directives.unchanged }
flickr.content = 1

# Simply importing this module will make the directive available.
docutils.parsers.rst.directives.register_directive( 'flickr', flickr )

if __name__ == "__main__":
  import docutils.core
  docutils.core.publish_cmdline(writer_name='html')
