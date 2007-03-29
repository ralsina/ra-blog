# -*- coding: utf-8 -*-

import urllib

class Talkr:
    def __init__(self,blog):
        self.blog=blog
        self.talkrFeedID="15734"
            
    def link(self,post):
        return u'''
            <a href='http://www.talkr.com/app/fetch.app?feed_id=%s&perma_link=%s'>Listen to this post</a>
            '''%(self.talkrFeedID,urllib.quote(post.myurl()))
            
    def chiclet(self):
        return u'''
            <a href='http://www.talkr.com/app/cast_pods.app?feed_id=%s'>
                <img src='http://images.talkr.com/images/xml-podcast.gif' alt='Link to Podcast (RSS feed) for this blog' border='0'>
            </a>'''%self.talkrFeedID
        

def factory(blog):
    return Talkr(blog)
