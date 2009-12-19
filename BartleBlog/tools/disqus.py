# -*- coding: utf-8 -*-

import BartleBlog.backend.dbclasses as db

class Disqus:
    def __init__(self,blog):
        self.blog=blog
        self.user='ralsina'

    def head(self):
        return []

    def commentLink(self, post):
        url=self.blog.macros.absoluteUrl(post.myurl())
        return '<a href="%s#disqus_thread">Comments</a>'%url

    def commentCounter(self):
        return u'''
<script type="text/javascript">
//<![CDATA[
(function() {
    var links = document.getElementsByTagName('a');
    var query = '?';
    for(var i = 0; i < links.length; i++) {
    if(links[i].href.indexOf('#disqus_thread') >= 0) {
        query += 'url' + i + '=' + encodeURIComponent(links[i].href) + '&';
    }
    }
    document.write('<script charset="utf-8" type="text/javascript" src="http://disqus.com/forums/lateralopinion/get_num_replies.js' + query + '"></' + 'script>');
})();
//]]>
</script>
        '''


def factory(blog):
    return Disqus(blog)
