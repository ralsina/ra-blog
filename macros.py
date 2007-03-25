import datetime
# -*- coding: utf-8 -*-


basepath=u"http://lateral.blogsite.org/"
author=u"Roberto Alsina <ralsina@kde.org>"

def weblogPermaLink(post):
    date=post.pubDate
    return u"%sweblog/%s/%02d/%02d.html#%s"%(basepath,date.year,date.month,date.day,post.postID)

def getUrlForDay(date):
    return u"%sweblog/%s/%02d/%02d.html"%(basepath,date.year,date.month,date.day)

def absoluteUrl(path):
    return basepath+path

def copyright(year):
    return u"&copy; %d-%d %s"%(year,datetime.date.today().year,author)
    
chunk={
'first': u'''
''',
'second':u'''
<span>
All contents of this site written by me are free.<p> 
Copy, modify, whatever., just put my name in it, and if you change the contents, 
clearly say so in the same page. Please provide a link back to the original.
</span><p>
<b>Latest Comments:</b><br>
<script type="text/javascript" src="http://www.haloscan.com/members/recent/ralsina/"> </script>
<style type="text/css">
#haloscan-recent { padding: 2px; margin: 2px; }
#haloscan-recent a { text-decoration: none; color: #333333;}
#haloscan-recent ul {  list-style: none; width: 100%; overflow: hidden; margin: 0; padding: 0;}
#haloscan-recent li { text-align: justify; list-style: none; margin: 1px;}
#haloscan-recent li span.hsrname { color: #06c; font-weight: bold; }
#haloscan-recent li span.hsrmsg { font-weight: normal; }
</style>
<p style="align:right;">
<!-- Start of StatCounter Code -->
<script type="text/javascript" language="javascript">
var sc_project=1436219; 
var sc_invisible=0; 
var sc_partition=13; 
var sc_security="b91cd70a"; 
</script>

<script type="text/javascript" language="javascript" src="http://www.statcounter.com/counter/counter.js"></script><noscript><a href="http://www.statcounter.com/" target="_blank"><img  src="http://c14.statcounter.com/counter.php?sc_project=1436219&amp;java=0&amp;security=b91cd70a&amp;invisible=0" alt="hitcounter" border="0"></a> </noscript>
<a href="http://my.statcounter.com/project/standard/stats.php?project_id=1436219&amp;guest=1">Stats</a>
<!-- End of StatCounter Code -->
<br>

<a href="http://feeds.feedburner.com/LateralOpinion"><img src="http://feeds.feedburner.com/~fc/LateralOpinion?bg=99CCFF&amp;fg=444444&amp;anim=1" height="26" width="88" style="border:0" alt="" /></a>
<br>
<a href='http://www.talkr.com/app/cast_pods.app?feed_id=15734'>
    <img src='http://images.talkr.com/images/xml-podcast.gif' alt='Link to Podcast (RSS feed) for this blog' border='0'>
</a>
'''
}
