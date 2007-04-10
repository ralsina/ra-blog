# -*- coding: utf-8 -*-

class Mootools:
    def __init__(self,blog):
        self.blog=blog
    def head(self):
        return ['<script type="text/javascript" charset="utf-8" src="%s" ></script>'%self.blog.macros.absoluteUrl('static/js/mootools.js')]

def factory (blog):
    return Mootools(blog)
