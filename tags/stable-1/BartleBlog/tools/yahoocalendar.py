# -*- coding: utf-8 -*-

import BartleBlog.backend.dbclasses as db
import os,codecs


class YahooCalendar:
    def __init__(self,blog):
        self.blog=blog
        self.blog.monthHooks.append(self.renderMonth)

    def monthScript(self,_date):
        date=_date.replace(day=1)
        if date.month==12:
            nextmonth=date.replace(year=date.year+1,month=1)
        else:
            nextmonth=date.replace(month=date.month+1)
        disabled = ['%d/%d/%d'%(date.month,x,date.year) for x in range(1,32)]
        monthposts=db.Post.select(db.AND(db.Post.q.pubDate>=date,db.Post.q.pubDate<nextmonth))
        selected=[]
        for post in monthposts:
            s='%d/%d/%d'%(post.pubDate.month,post.pubDate.day,post.pubDate.year)
            selected.append(s)
            if s in disabled:
                disabled.remove(s)
        disabled=','.join(disabled)
        return '''YAHOO.namespace("blog");
                        function cal1_init() {
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
                              
                            var changeMonth = function(type,args,obj) {
                            };
                            YAHOO.blog.cal1.selectEvent.subscribe(selectedDate, YAHOO.blog.cal1, true);
                            YAHOO.blog.cal1.changePageEvent.subscribe(changeMonth, YAHOO.blog.cal1, true);

                            YAHOO.blog.cal1.render();
                        }
                        YAHOO.util.Event.onDOMReady (cal1_init);
                '''%(date.month,date.year,disabled,self.blog.basepath)

    def monthScriptTag(self,date):
        return '<script type="text/javaScript" src="%s"></script>'%self.blog.macros.absoluteUrl('static/js/calendar/%s-%s.js'%(date.year,date.month))
        
    def renderMonth(self,date):
        dname=os.path.join(self.blog.dest_dir, 'static/js/calendar')
        fname='%s-%s.js'%(date.year,date.month)
        print "rendering calendar",os.path.join(dname,fname)
        f=codecs.open(os.path.join(dname,fname),"w","utf-8")
        f.write(self.monthScript(date))
        
        
    def head(self):
        return [
        '<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.3.0/build/calendar/assets/skins/sam/calendar.css">', 
        '<script type="text/javascript" src="http://yui.yahooapis.com/2.3.0/build/yahoo-dom-event/yahoo-dom-event.js"></script>', 
        '<script type="text/javascript" src="http://yui.yahooapis.com/2.3.0/build/calendar/calendar-min.js"></script>', 
        '<script type="text/javaScript" src="%s"></script>'%self.blog.macros.absoluteUrl('static/js/sprintf.js')
        ]

    def widget(self,_date):
        return '<div id="cal1Container class="yui-skin-sam"></div>'



def factory(blog):
    return YahooCalendar(blog)
