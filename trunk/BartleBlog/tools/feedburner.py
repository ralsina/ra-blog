# -*- coding: utf-8 -*-

import BartleBlog.backend.dbclasses as db

class FeedBurner:
    def __init__(self,blog):
        self.blog=blog
        self.feedburnerName="LateralOpinion"
        self.feedburnerStoriesName="LateralOpinionStories"

    def rssUrl(self):
        return 'http://feeds.feedburner.com/%s'%self.feedburnerName

    def rssHead(self):
        return ['<link rel="alternate" type="application/rss+xml" title="RSS" href="%s">'%self.rssUrl()]

    def counter(self):
        return '''
    <a href="http://feeds.feedburner.com/%s"><img src="http://feeds.feedburner.com/~fc/%s?bg=99CCFF&amp;fg=444444&amp;anim=1" height="26" width="88" style="border:0" alt="" /></a>
    '''%(self.feedburnerName,self.feedburnerName)

    def flare(self,post):
        if isinstance(post,db.Story):
            n=self.feedburnerStoriesName
        else:
            n=self.feedburnerName
        return u'''
            <script src="http://feeds.feedburner.com/~s/%s?i=%s" type="text/javascript" charset="utf-8"></script>
            '''%(n,post.myurl().replace('#','%23'))

    def banner(self):
        return u'''
        <td align=center>
          <a href=http://feeds.feedburner.com/%s">
            <img src="http://feeds.feedburner.com/%s.gif" alt="%s" style="border:0">
          </a>
        </td>
    '''%(self.feedburnerName,self.feedburnerName,self.blog.blogName)


def factory(blog):
    return FeedBurner(blog)
