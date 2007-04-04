# -*- coding: utf-8 -*-

import urllib

class AddThisTool:
    def __init__(self,blog):
        self.blog=blog
        self.user='ralsina'

    def head(self):
        return []

    def bookmark(self,post):
        return '''
<a href="http://www.addthis.com/bookmark.php" onclick="window.open('http://www.addthis.com/bookmark.php?wt=nw&pub=%s&url=%s&title=%s', 'addthis', 'scrollbars=yes,menubar=no,width=620,height=520,resizable=yes,toolbar=no,location=no,status=no,screenX=200,screenY=100,left=200,top=100'); return false;" title="Bookmark using any bookmark manager!" target="_blank"><img src="http://s3.addthis.com/button1-bm.gif" width="125" height="16" border="0" alt="AddThis Social Bookmark Button" /></a>
'''.replace('&','&amp;')%(self.user,urllib.quote(self.blog.macros.absoluteUrl(post.myurl())),post.title)

    def subscribe(self):
        return '''
<a href="http://www.addthis.com/feed.php?pub=%s&h1=%s&t1=" title="Subscribe using any feed reader!"><img src="http://s3.addthis.com/button1-rss.gif" width="125" height="16" border="0" alt="AddThis Feed Button" /></a>
'''%(self.user,urllib.quote(self.blog.macros.feedBurner.rssUrl()))


def factory (blog):
    return AddThisTool(blog)
