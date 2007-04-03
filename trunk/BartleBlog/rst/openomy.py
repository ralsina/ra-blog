# -*- coding: utf-8 -*-

import docutils.core
import docutils.parsers.rst
import os,sys

from BartleBlog.util.openomy import *

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
        op=Openomy()
        tag=op.Tags_GetTag(tname)
        html='<table class="openomy_table">'
        
        for file_id in tag.files:
            print "===>",file_id
            f=op.Files_GetFile(file_id)
            html+='<tr><td>Download: </td><td><a href="%s">%s</a></td></tr>'%(f.url,f.filename)
            
        html+='</table>'


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
        
        op=Openomy()
        f=op.Files_GetFile(fname)
        if not f:
            error = state_machine.reporter.error('No file %s in openomy.com'%fname,
            docutils.nodes.literal_block(block_text, block_text), line=lineno )
            return [error]

        if not f.public:
            error = state_machine.reporter.error('The file %s is not public'%fname,
            docutils.nodes.literal_block(block_text, block_text), line=lineno )
            return [error]
                
        html='<a href="%s">%s</a>'%(f.url,f.filename)
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
