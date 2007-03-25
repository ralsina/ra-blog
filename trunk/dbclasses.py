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
    def HaloScanComments(self):
        return u'''
          <a href="javascript:HaloScan('%s');" target="_self">
          <script type="text/javascript">postCount('%s');</script></a>'''%(self.postID,self.postID)
    def HaloScanTB(self):
        return u'''
        <a href="javascript:HaloScanTB('%s');" target="_self">
        <script type="text/javascript">postCountTB('%s'); </script></a>'''%(self.postID,self.postID)
    def Talkr(self):
        return u'''
        <a href='http://www.talkr.com/app/fetch.app?feed_id=15734&perma_link=%s'>Listen to this post</a>
        '''%urllib.quote(self.myurl())
    def FeedBurnerFlare(self):
        return u'''
        <script src="http://feeds.feedburner.com/~s/LateralOpinion?i=%s" type="text/javascript" charset="utf-8"></script>
        '''%(self.myurl().replace('#','%23'))
        
    def TechnoratiTags(self):
        tags=['<a href="http://technorati.com/tag/%s">%s</a>'%(x.nameID,x.nameID) for x in self.categories]
        if tags:
            return u"Topics: "+", ".join(tags)
        return u""
        
    
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
    def HaloScanComments(self):
        return '''
          <a href="javascript:HaloScan('STORY%s');" target="_self">
          <script type="text/javascript">postCount('STORY%s');</script></a>'''%(self.postID,self.postID)
    def HaloScanTB(self):
        return '''
        <a href="javascript:HaloScanTB('STORY%s');" target="_self">
        <script type="text/javascript">postCountTB('STORY%s'); </script></a>'''%(self.postID,self.postID)
