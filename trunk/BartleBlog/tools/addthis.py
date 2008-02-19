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

<!-- AddThis Button BEGIN -->
<script type="text/javascript">addthis_pub  = '%s';</script>
<a href="http://www.addthis.com/bookmark.php" onMouseOver="return addthis_open(this, '', '%s', '%s')" onMouseOut="addthis_close()" onClick="return addthis_sendto()"><img src="http://s9.addthis.com/button1-share.gif" width="125" height="16" border="0" alt="" /></a><script type="text/javascript" src="http://s7.addthis.com/js/152/addthis_widget.js"></script>
<!-- AddThis Button END -->
'''.replace('&','&amp;')%(self.user,urllib.quote(self.blog.macros.absoluteUrl(post.myurl())),post.title)

    def subscribe(self):
        return '''
<a href="http://www.addthis.com/feed.php?pub=%s&h1=%s&t1=" title="Subscribe using any feed reader!"><img src="http://s3.addthis.com/button1-rss.gif" width="125" height="16" border="0" alt="AddThis Feed Button" /></a>
'''.replace('&','&amp;')%(self.user,urllib.quote(self.blog.macros.feedBurner.rssUrl()))


def factory (blog):
    return AddThisTool(blog)
