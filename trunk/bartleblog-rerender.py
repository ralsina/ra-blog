#!/usr/bin/env python

try:
    import psyco
    psyco.full()
except:
    pass

import BartleBlog.backend.blog as blog
b=blog.Blog()
b.renderFullBlog()
