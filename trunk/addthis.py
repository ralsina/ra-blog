# -*- coding: utf-8 -*-

class AddThisTool:
    def __init__(self,blog):
        self.blog=blog
        self.user='ralsina'
        
    def head(self):
        return []
        
    def button(self):
        return '''
    <!-- AddThis Bookmark Button BEGIN -->
    <div>
    <a href="http://www.addthis.com/bookmark.php" onclick="window.open('http://www.addthis.com/bookmark.php?wt=nw&pub=%s&url='+encodeURIComponent(location.href)+'&title='+encodeURIComponent(document.title), 'addthis', 'scrollbars=yes,menubar=no,width=620,height=520,resizable=yes,toolbar=no,location=no,status=no,screenX=200,screenY=100,left=200,top=100'); return false;" title="Bookmark using any bookmark manager!" target="_blank"><img src="http://s3.addthis.com/button1-bm.gif" width="125" height="16" border="0" alt="AddThis Social Bookmark Button" /></a></div>
    <!-- AddThis Bookmark Button END -->'''%self.user
        

def factory (blog):
    return AddThisTool(blog)
    
