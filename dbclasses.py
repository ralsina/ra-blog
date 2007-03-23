from sqlobject import *

class Categories(SQLObject):
    name=StringCol()
    
class PostCategories(SQLObject):
    postID=ForeignKey('Post')
    name=ForeignKey('Categories')

class StoryCategories(SQLObject):
    postID=ForeignKey('Story')
    name=ForeignKey('Categories')

class Post(SQLObject):
    postID=StringCol()
    title=StringCol()
    link=StringCol()
    source=StringCol()
    sourceUrl=StringCol()
    text=StringCol()
    rendered=StringCol()
    onHome=BoolCol()
    structured=BoolCol()
    pubDate=DateTimeCol()
    categories=MultipleJoin('PostCategories')
    
class Story(SQLObject):
    postID=StringCol()
    pubDate=DateTimeCol()
    title=StringCol()
    desc=StringCol()
    text=StringCol()
    rendered=StringCol()
    structured=BoolCol()
    draft=BoolCol()
    quiet=BoolCol()
    categories=MultipleJoin('StoryCategories')
