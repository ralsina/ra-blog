# -*- coding: utf-8 -*-

import docutils.core
import docutils.parsers.rst
import BartleBlog.util.hq23api as hq23api


flickrAPIKey='a4b67aa4c75657b2db3ebc2f2f43c136'
fapi=hq23api.FlickrAPI(flickrAPIKey,'ab116226d50899a7')


def flickrset( name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine ):
    """
    A directive that produces a table with all thepictures in a flickr set in HTML.

    The syntax is this::

        .. flickrset:: setname

    Where setname is the name of the set in flickr.
    """
    
    
def htmlforphoto(photo,fname):
    token = fapi.getToken(browser="firefox")
    id=photo['id']
    secret=photo['secret']
    owner=photo['owner']
    rsp = fapi.photos_getInfo(api_key=flickrAPIKey,auth_token=token,photo_id=id,secret=secret)

    farm=rsp.photo[0]['farm']
    server=rsp.photo[0]['server']


    url= 'http://www.23hq.com/photos/%s/%s'%(owner,id)
    t_url='http://farm%s.static.23hq.com/%s/%s_%s_%s.jpg'%(
            farm,server,id,secret,'m')

    html='<div class="center"><a href="%s"><img src="%s" class="flickr" alt="%s"></a><div class="footerbox">%s</div></div>'%(url,t_url,fname,fname)
    return html

def flickr( name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine ):
    """
    A directive that produces a nicely styled image from flickr in HTML.

    The syntax is this::

        .. 23hq:: title

    Where title is the title you used in 23hq.
    """

    token = fapi.getToken(browser="firefox")
    fname=arguments[0]
    rsp = fapi.photos_search(api_key=flickrAPIKey,auth_token=token,user_id='me',text=fname)

    # Get the secret and ID of the photo
    try:
        photo=rsp.photos[0].photo[0]
    except AttributeError:
        error = state_machine.reporter.error( "Can't find image called %s in 23hq"% fname,
                    docutils.nodes.literal_block(block_text, block_text), line=lineno )
        return [error]
        

    html=htmlforphoto(photo,fname)

    raw = docutils.nodes.raw('',html, format = 'html')
    return [raw]

flickr.arguments = (1,0,0)
flickr.options = {'name' : docutils.parsers.rst.directives.unchanged }
flickr.content = 1

# Simply importing this module will make the directive available.
docutils.parsers.rst.directives.register_directive( '23hq', flickr )

if __name__ == "__main__":
    import docutils.core
    docutils.core.publish_cmdline(writer_name='html')
