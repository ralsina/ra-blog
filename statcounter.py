# -*- coding: utf-8 -*-


class StatCounter:
    def __init__(self,blog):
        self.blog=blog
        self.project='1436219'

    def chiclet(self):
        return '''
            <!-- Start of StatCounter Code -->
            <script type="text/javascript" language="javascript">
            var sc_project=%s;
            var sc_invisible=0;
            var sc_partition=13;
            var sc_security="b91cd70a";
            </script>
            <script type="text/javascript" language="javascript" src="http://www.statcounter.com/counter/counter.js"></script>
            <noscript>
              <a href="http://www.statcounter.com/" target="_blank"><img  src="http://c14.statcounter.com/counter.php?sc_project=%s&amp;java=0&amp;security=b91cd70a&amp;invisible=0" alt="hitcounter" border="0"></a>
            </noscript>
            <a href="http://my.statcounter.com/project/standard/stats.php?project_id=%s&amp;guest=1">Stats</a>
    '''%(self.project,self.project,self.project)

def factory (blog):
    return StatCounter(blog)
