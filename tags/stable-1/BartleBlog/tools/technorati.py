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
            
    def topTags(self):
        return '''\
        <script src="http://widgets.technorati.com/t.js" type="text/javascript"> </script>
        <a href="http://technorati.com/blogs/%s?sub=tr_tagcloud_t_ns" class="tr_tagcloud_t_js" style="color:#4261DF">View blog top tags</a>
        '''%self.blog.basepath
        
    def linkCount(self, url):
        return '''\
        <script src="http://embed.technorati.com/linkcount" type="text/javascript"></script>
        <a class="tr-linkcount" href="http://technorati.com/search/%s">View blog reactions</a>
        '''%url

def factory(blog):
    return Technorati(blog)
