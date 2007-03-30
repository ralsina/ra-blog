# -*- coding: utf-8 -*-
import docutils.core

import rstcode
import rstflickr

def rst2html(rst):
    return docutils.core.publish_parts(rst,writer_name='html')['fragment']

