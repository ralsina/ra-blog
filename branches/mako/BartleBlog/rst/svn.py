# -*- coding: utf-8 -*-

import docutils.core
import docutils.parsers.rst
import os,sys
import elementtree.ElementTree as tree
from StringIO import StringIO
from rst2html import rst2html
from cgi import escape
import time

def directive_svnlog (name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine ):
    """
    A directive that produces a formatted SVN log 

    The syntax is this::

    .. svnlog:: repository
        :limit: 10

    Where tagname is the argument used for "svn log" and limit is the
    maximum number of entries.
    """
    path=arguments[0]
    cmd='svn log %s --xml --non-interactive '%path
    if options.has_key('limit'):
        cmd+='--limit '+options['limit']
    p=os.popen(cmd)
    data=p.read()
    err=p.close()

    f=StringIO(data)
    t=tree.parse(f)
    r=t.getroot()
    
    formatted=[]
    entries=r.findall('logentry')
        
    for entry in entries:
        date=entry.find('date').text
        msg,code=rst2html(entry.find('msg').text)
        if -1<>code:
            msg='<pre>%s</pre>'%(escape(entry.find('msg').text))
        author=entry.find('author').text
        rev=entry.attrib['revision']
        formatted.append('''
        <div>        
        <h4>%s: revision %s by %s</h4><p>
        %s
        </div>
        '''%(date,rev,author,msg))
        
    html='\n\n'.join(formatted)
    
    raw = docutils.nodes.raw('',html, format = 'html')
    return [raw]


directive_svnlog.arguments = (1,0,0)
directive_svnlog.options = {'name' : docutils.parsers.rst.directives.unchanged, 
                            'limit': docutils.parsers.rst.directives.unchanged }
directive_svnlog.content = 1

# Simply importing this module will make the directive available.
docutils.parsers.rst.directives.register_directive( 'svnlog', directive_svnlog )

if __name__ == "__main__":
    import docutils.core
    docutils.core.publish_cmdline(writer_name='html')
