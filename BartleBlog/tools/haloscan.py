# -*- coding: utf-8 -*-

import BartleBlog.backend.dbclasses as db

class HaloScan:
    def __init__(self,blog):
        self.blog=blog
        self.user='ralsina'

    def head(self):
        return ['<script type="text/javascript" src="http://www.haloscan.com/load/%s"> </script>'%self.user]

    def comments(self,post):
        if isinstance(post,db.Story):
            id="STORY"+post.postID
        else:
            id=post.postID
        return u'''
            <a href="javascript:HaloScan('%s');">
            <script type="text/javascript">postCount('%s');</script></a>'''%(id,id)

    def trackback(self,post):
        if isinstance(post,db.Story):
            id="STORY"+post.postID
        else:
            id=post.postID
        return u'''
            <a href="javascript:HaloScanTB('%s');">
            <script type="text/javascript">postCountTB('%s'); </script></a>'''%(id,id)

    def comments_and_trackbacks(self, post, separator='&nbsp;&bull;&nbsp;'):
        if isinstance(post,db.Story):
            id="STORY"+post.postID
        else:
            id=post.postID
        return u'''
            <script type="text/javascript">
            document.write('<a href="javascript:HaloScan(\\'%s\\');">');
            postCount('%s');
            document.write('</a>%s');
            document.write('<a href="javascript:HaloScanTB(\\'%s\\');">');
            postCountTB('%s');
            document.write('</a>');
            </script>'''%(id,id,separator,id,id)

    def latestComments(self):
        return u'''
            <b>Latest Comments:</b><br>
            <script type="text/javascript" src="http://www.haloscan.com/members/recent/%s/"> </script>
            <style type="text/css">
            #haloscan-recent { padding: 2px; margin: 2px; }
            #haloscan-recent a { text-decoration: none; color: #333333;}
            #haloscan-recent ul {  list-style: none; width: 100%%; overflow: hidden; margin: 0; padding: 0;}
            #haloscan-recent li { text-align: justify; list-style: none; margin: 1px;}
            #haloscan-recent li span.hsrname { color: #06c; font-weight: bold; }
            #haloscan-recent li span.hsrmsg { font-weight: normal; }
            </style>
        '''%self.user

    def chiclet(self):
        return u'''
        <a href="http://www.haloscan.com/">
        <img width="88" height="31" src="http://www.haloscan.com/halolink.gif" border="0" alt="Weblog Commenting and Trackback by HaloScan.com" />
        </a>'''



def factory(blog):
    return HaloScan(blog)
