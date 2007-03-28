# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import datetime
from dbclasses import *
head=[]

#################################################################################
### Things that should be in the config file
#################################################################################

blogName="Lateral Opinion"
basepath=u"http://lateral.blogsite.org/"
author=u"Roberto Alsina"
author_email=u"ralsina@kde.org"
description=u"Roberto Alsina's blog"
language="en"
version="Bartleblog 0.0"
feedburnerName="LateralOpinion"
feedburnerStoriesName="LateralOpinionStories"
haloscanUser="ralsina"
talkrFeedID="15734"
addthisUser="ralsina"

#################################################################################
### <head> manipulation
#################################################################################

def addHead(headers):
    global head
    for h in headers:
        if not h in head:
            head.append(h)

def insertHead():
    return '\n'.join(head)

def rstHead():
    return [
    '<link rel="stylesheet" type="text/css" href="%s">'%absoluteUrl('static/css/rst.css'),
    '<link rel="stylesheet" type="text/css" href="%s">'%absoluteUrl('static/css/html.css'),
    '<link rel="stylesheet" type="text/css" href="%s">'%absoluteUrl('static/css/bartleblog.css'),
    '<link rel="stylesheet" type="text/css" href="%s">'%absoluteUrl('static/css/silvercity.css')
    ]
    
#################################################################################
### General Macros
#################################################################################
    
def weblogPermaLink(post):
    date=post.pubDate
    return u"%sweblog/%s/%02d/%02d.html#%s"%(basepath,date.year,date.month,date.day,post.postID)

def getUrlForDay(date):
    return u"%sweblog/%s/%02d/%02d.html"%(basepath,date.year,date.month,date.day)

def absoluteUrl(path):
    return basepath+path

def copyright(rss=False):
    earliest=Post.select(orderBy=Post.q.pubDate)[0].pubDate
    if rss:
        return u"Copyright %d-%d %s"%(earliest.year,datetime.date.today().year,author)
    return u"&copy; %d-%d %s <%s>"%(earliest.year,datetime.date.today().year,author,author_email)

#################################################################################
### Morgle Macros
#################################################################################
    
#################################################################################
### AddThis Macros
#################################################################################

def addthisButton():
    return '''
<!-- AddThis Bookmark Button BEGIN -->
<div>
<a href="http://www.addthis.com/bookmark.php" onclick="window.open('http://www.addthis.com/bookmark.php?wt=nw&pub=%s&url='+encodeURIComponent(location.href)+'&title='+encodeURIComponent(document.title), 'addthis', 'scrollbars=yes,menubar=no,width=620,height=520,resizable=yes,toolbar=no,location=no,status=no,screenX=200,screenY=100,left=200,top=100'); return false;" title="Bookmark using any bookmark manager!" target="_blank"><img src="http://s3.addthis.com/button1-bm.gif" width="125" height="16" border="0" alt="AddThis Social Bookmark Button" /></a></div>
<!-- AddThis Bookmark Button END -->'''%addthisUser

    
#################################################################################
### Technorati Macros
#################################################################################

    
def technoratiSearch():
    return '''
      <script type="text/javascript" src="http://embed.technorati.com/embed/tpgux8rtif.js"></script>
    '''

def technoratiTags(post):
    tags=['<a href="http://technorati.com/tag/%s">%s</a>'%(x.name,x.name) for x in post.categories]
    if tags:
        return u"Topics: "+", ".join(tags)
    return u""

    
#################################################################################
### Yahoo Grids (layout)
#################################################################################
    
def yahooGridsHead():
    return ['<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.2.0/build/reset-fonts-grids/reset-fonts-grids.css">']
    
#################################################################################
### Yahoo Calendar widget
#################################################################################
        
def yahooCalendarHead():
    return [
    '<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.2.0/build/calendar/assets/calendar.css">',
    '<script type="text/javascript" src="http://yui.yahooapis.com/2.2.0/build/yahoo-dom-event/yahoo-dom-event.js"></script>',
    '<script type="text/javascript" src="http://yui.yahooapis.com/2.2.0/build/calendar/calendar-min.js"></script>',
    '<script type="text/JavaScript" src="%s"></script>'%absoluteUrl('static/js/sprintf.js')
    ]
        
def yahooCalendarWidget(_date):
    date=_date.replace(day=1)
    if date.month==12:
        nextmonth=date.replace(year=date.year+1,month=1)
    else:
        nextmonth=date.replace(month=date.month+1)
    disabled = ['%d/%d/%d'%(date.month,x,date.year) for x in range(1,32)]
    monthposts=Post.select(AND(Post.q.pubDate>=date,Post.q.pubDate<nextmonth))
    selected=[]
    for post in monthposts:
        s='%d/%d/%d'%(post.pubDate.month,post.pubDate.day,post.pubDate.year)
        selected.append(s)
        if s in disabled:
            disabled.remove(s)
    disabled=','.join(disabled)
    
    return '''  <div id="cal1Container"></div>
                <script>
                    YAHOO.namespace("blog");
                    function init() {
                        YAHOO.blog.cal1 = 
                            new YAHOO.widget.Calendar("cal1","cal1Container", {
                                pagedate:"%d/%d"
                                });
                        YAHOO.blog.cal1.addRenderer("%s",YAHOO.blog.cal1.renderBodyCellRestricted);
                        
                        var selectedDate = function (type,args,obj) {
                            var s1 = args[0];
                            var s2 = s1[0];
                            window.location=printf("%s/weblog/%%d/%%02d/%%02d.html",s2[0],s2[1],s2[2]);
                        };                    
                        YAHOO.blog.cal1.selectEvent.subscribe(selectedDate, YAHOO.blog.cal1, true);

                        YAHOO.blog.cal1.render();
                    }
                    YAHOO.util.Event.addListener(window, "load", init);
                </script>
            '''%(date.month,date.year,disabled,basepath)

#################################################################################
### HaloScan Macros
#################################################################################
            
def haloscanHead():
    return ['<script type="text/javascript" src="http://www.haloscan.com/load/%s"> </script>'%haloscanUser]

def haloscanComments(post):
    if isinstance(post,Story):
        id="STORY"+post.postID
    else:
        id=post.postID
    return u'''
        <a href="javascript:HaloScan('%s');" target="_self">
        <script type="text/javascript">postCount('%s');</script></a>'''%(id,id)

def haloscanTB(post):
    if isinstance(post,Story):
        id="STORY"+post.postID
    else:
        id=post.postID
    return u'''
        <a href="javascript:HaloScanTB('%s');" target="_self">
        <script type="text/javascript">postCountTB('%s'); </script></a>'''%(id,id)

def haloscanLatestComments():            
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
    '''%haloscanUser

def haloscanChiclet():
    return u'''
    <a href="http://www.haloscan.com/">
    <img width="88" height="31" src="http://www.haloscan.com/halolink.gif" border="0" alt="Weblog Commenting and Trackback by HaloScan.com" />
    </a>'''
    
#################################################################################
### StatCounter Macros
#################################################################################
    
def statcounterChiclet():
    return '''
        <!-- Start of StatCounter Code -->
        <script type="text/javascript" language="javascript">
        var sc_project=1436219; 
        var sc_invisible=0; 
        var sc_partition=13; 
        var sc_security="b91cd70a"; 
        </script>
        <script type="text/javascript" language="javascript" src="http://www.statcounter.com/counter/counter.js"></script>
        <noscript>
          <a href="http://www.statcounter.com/" target="_blank"><img  src="http://c14.statcounter.com/counter.php?sc_project=1436219&amp;java=0&amp;security=b91cd70a&amp;invisible=0" alt="hitcounter" border="0"></a> 
        </noscript>
        <a href="http://my.statcounter.com/project/standard/stats.php?project_id=1436219&amp;guest=1">Stats</a>
'''

#################################################################################
### FeedBurner Macros
#################################################################################

def feedburnerHead():
    return ['<link rel="alternate" type="application/rss+xml" title="RSS" href="http://feeds.feedburner.com/%s">'%feedburnerName]
    
def feedburnerCounter():
    return '''
<a href="http://feeds.feedburner.com/LateralOpinion"><img src="http://feeds.feedburner.com/~fc/LateralOpinion?bg=99CCFF&amp;fg=444444&amp;anim=1" height="26" width="88" style="border:0" alt="" /></a>
'''

def feedburnerFlare(post):
    if isinstance(post,Story):
        n=feedburnerStoriesName
    else:
        n=feedburnerName
    return u'''
        <script src="http://feeds.feedburner.com/~s/%s?i=%s" type="text/javascript" charset="utf-8"></script>
        '''%(n,post.myurl().replace('#','%23'))

def feedburnerBanner():
    return u'''
    <td align=center>
      <a href=http://feeds.feedburner.com/%s">
        <img src="http://feeds.feedburner.com/%s.gif" alt="%s" style="border:0">
      </a>
    </td>    
'''%(feedburnerName,feedburnerName,blogName)
        
#################################################################################
### Talkr Macros
#################################################################################

def talkrLink(post):
    return u'''
        <a href='http://www.talkr.com/app/fetch.app?feed_id=%s&perma_link=%s'>Listen to this post</a>
        '''%(talkrFeedID,urllib.quote(post.myurl()))
        
def talkrChiclet():
    return u'''
        <a href='http://www.talkr.com/app/cast_pods.app?feed_id=%s'>
            <img src='http://images.talkr.com/images/xml-podcast.gif' alt='Link to Podcast (RSS feed) for this blog' border='0'>
        </a>'''%talkrFeedID


chunk={
'blurb':u'''
All contents of this site written by me are free.
Copy, modify, whatever., just put my name in it, and if you change the contents, 
clearly say so in the same page. Please provide a link back to the original.

'''
}
