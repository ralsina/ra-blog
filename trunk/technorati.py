# -*- coding: utf-8 -*-


class Technorati:
    def __init__(self,blog):
        self.blog=blog

    def search(self):
        return '''
          <script type="text/javascript" src="http://embed.technorati.com/embed/tpgux8rtif.js"></script>
        '''
    
    def tags(self,post):
        tags=['<a href="http://technorati.com/tag/%s">%s</a>'%(x.name,x.name) for x in post.categories]
        if tags:
            return u"Topics: "+", ".join(tags)
        return u""

def factory(blog):
    return Technorati(blog)
