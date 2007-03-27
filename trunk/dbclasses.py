# -*- coding: utf-8 -*-

from sqlobject import *
import urllib

class Categories(SQLObject):
    name=UnicodeCol()
    
class PostCategories(SQLObject):
    postID=ForeignKey('Post')
    name=ForeignKey('Categories')

class StoryCategories(SQLObject):
    storyID=ForeignKey('Story')
    name=ForeignKey('Categories')

class Post(SQLObject):
    postID=UnicodeCol()
    title=UnicodeCol()
    link=UnicodeCol()
    source=UnicodeCol()
    sourceUrl=UnicodeCol()
    text=UnicodeCol()
    rendered=UnicodeCol()
    onHome=BoolCol()
    structured=BoolCol()
    pubDate=DateTimeCol()
    categories=MultipleJoin('PostCategories')
    def myurl(self):
        return u"http://lateral.blogsite.org/weblog/%d/%02d/%02d.html#%s"%(self.pubDate.year,
                                                                      self.pubDate.month,
                                                                      self.pubDate.day,
                                                                      self.postID)
            
class Story(SQLObject):
    postID=UnicodeCol()
    pubDate=DateTimeCol()
    title=UnicodeCol()
    desc=UnicodeCol()
    text=UnicodeCol()
    rendered=UnicodeCol()
    structured=BoolCol()
    draft=BoolCol()
    quiet=BoolCol()
    categories=MultipleJoin('StoryCategories')
    def myurl(self):
        return "http://lateral.blogsite.org/stories/%s.html"%self.postID
