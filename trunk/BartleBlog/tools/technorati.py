# -*- coding: utf-8 -*-

import BartleBlog.backend.config as config

class Technorati:
    def __init__(self,blog):
        self.blog=blog
        self.user=config.getValue('technorati', 'username', None)

    def tags(self,post):
        tags=['<a href="http://technorati.com/tag/%s">%s</a>'%(x.name,x.name) for x in post.categories]
        if tags:
            return u"Topics: "+", ".join(tags)
        return u""

    def favorites(self):
        if self.user:
            return '''<iframe src="http://widgets.technorati.com/faves/%s?t=posts" marginwidth="0" marginheight="0" height="400" width="100%%" frameborder="0" scrolling="auto" style="padding:0;border:none;" ></iframe>'''%self.user
        else:
            return '''<b>You need to configure the technorati support</b>'''

def factory(blog):
    return Technorati(blog)
