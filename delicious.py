# -*- coding: utf-8 -*-


class Delicious:
    def __init__(self,blog):
        self.blog=blog
        self.user='ralsina'
    
    def tags(self,post):
        tags=['<a href="http://del.icio.us/tag/%s">%s</a>'%(x.name,x.name) for x in post.categories]
        if tags:
            return u"Topics: "+", ".join(tags)
        return u""

def factory(blog):
    return Delicious(blog)
