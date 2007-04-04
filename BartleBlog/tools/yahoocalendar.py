# -*- coding: utf-8 -*-

import BartleBlog.backend.dbclasses as db


class YahooCalendar:
    def __init__(self,blog):
        self.blog=blog

    def head(self):
        return [
        '<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.2.0/build/calendar/assets/calendar.css">',
        '<script type="text/javascript" src="http://yui.yahooapis.com/2.2.0/build/yahoo-dom-event/yahoo-dom-event.js"></script>',
        '<script type="text/javascript" src="http://yui.yahooapis.com/2.2.0/build/calendar/calendar-min.js"></script>',
        '<script type="text/javaScript" src="%s"></script>'%self.blog.macros.absoluteUrl('static/js/sprintf.js')
        ]

    def widget(self,_date):
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

        return '''  <div id="cal1Container"></div>
                    <script type="text/javaScript">
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
                        if (window.addEventListener) window.addEventListener("load",init,false);
                        else if (window.attachEvent) window.attachEvent("onload",init);
                        /*YAHOO.util.Event.addListener(window, "load", init);*/
                    </script>
                '''%(date.month,date.year,disabled,self.blog.basepath)



def factory(blog):
    return YahooCalendar(blog)
