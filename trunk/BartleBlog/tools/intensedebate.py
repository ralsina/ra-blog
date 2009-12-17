# -*- coding: utf-8 -*-

import BartleBlog.backend.dbclasses as db

class IntenseDebate:
    def __init__(self,blog):
        self.blog=blog
        self.user='ralsina'

    def head(self):
        return []

    def comments(self,post):
        if isinstance(post,db.Story):
            id="STORY"+post.postID
        else:
            id=post.postID
        return u'''<script>
        var idcomments_acct = '8b0e31fe7776bceaad63dfc5e9c78f1b';
        var idcomments_post_id='%s';
        var idcomments_post_url='%s';
        </script>
        <script type="text/javascript" src="http://www.intensedebate.com/js/genericLinkWrapperV2.js"></script>
        '''%(id,post.myurl())

def factory(blog):
    return IntenseDebate(blog)
