# -*- coding: utf-8 -*-
import docutils.core

import codeblock
import flickr

def rst2html(rst):
    return docutils.core.publish_parts(rst,writer_name='html')['fragment']
