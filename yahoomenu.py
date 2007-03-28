# -*- coding: utf-8 -*-

menudesc='''
a 
b
c
 1
 2
  x
  y
d
'''

class menuitem:
    def __init__(self,parent,title,depth):
        self.parent=parent
        self.title=title
        self.children=[]
        self.depth=depth
        if parent:
            self.parent.children.append(self)
            
    def __repr__(self):
    
        if self.depth==0:
            return '''
            <div id="%s" class="yuimenubar">
                <div class="bd">
                    <ul class="first-of-type">
%s
                    </ul>
                </div>
            </div>
            '''%(self.title,'\n\n'.join([str(x) for x in self.children]))
            
            
        elif self.depth==1:
            if self.parent.children.index(self)==0:
                ss=" first-of-type"
            else:
                ss=""
            if not self.children:
                return '''
                        <li class="yuimenubaritem%s">%s</li>
                '''%(ss,self.title)
                        
            return '''
                        <li class="yuimenubaritem%s"> %s
                            <div id="%s" class="yuimenu">
                                <div class="bd">
                                    <ul>
%s
                                    </ul>
                                </div>
                            </div>
                        </li>
            '''%(ss,self.title,self.title,'\n\n'.join([str(x) for x in self.children]))
            
        elif self.depth>=2:
            if self.children:
                return '''
                                        <li class="yuimenuitem">%s
                                            <div id="%s" class="yuimenu">
                                                <div class="bd">
                                                    <ul class="first-of-type">
%s
                                                    </ul>
                                                </div>
                                            </div>
                                        </li>
                '''%(self.title,self.title,'\n\n'.join([str(x) for x in self.children]))
            return '''
                                        <li class="yuimenuitem">%s</li>
            '''%(self.title)
            
def linedepth(line):
    c=0
    while line[c]==' ':
        c=c+1
    return c

class YahooMenuTool:
    def __init__(self,blog):
        lines=menudesc.split('\n')
        curDepth=0
        self.root=menuitem(None,None,0)
        curItem=self.root
        for line in lines:
            if not line:
                continue
            d=linedepth(line)
            curItem=self.root
            for x in range(0,d):
                curItem=curItem.children[-1]
            menuitem(curItem,line,d+1)

    def menuBar(self):
        return str(self.root)
    
    def head(self):
        return [
            '<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.2.0/build/reset-fonts-grids/reset-fonts-grids.css">',
            '<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.2.0/build/menu/assets/menu.css">',
            '<script type="text/javascript" src="http://yui.yahooapis.com/2.2.0/build/yahoo-dom-event/yahoo-dom-event.js"></script>',
            '<script type="text/javascript" src="http://yui.yahooapis.com/2.2.0/build/container/container_core-min.js"></script>',
            '<script type="text/javascript" src="http://yui.yahooapis.com/2.2.0/build/menu/menu-min.js"></script>',
            '''
    <script type="text/javascript">
    YAHOO.example.onMenuBarReady = function(p_oEvent) 
    {
        // Instantiate and render the menu bar

        var oMenuBar = new YAHOO.widget.MenuBar("%s", 
            {   autosubmenudisplay:true, 
                hidedelay:750, 
                lazyload:true 
            });

        oMenuBar.render();
    }
    
    // Initialize and render the menu bar when it is available in the DOM
    YAHOO.util.Event.onContentReady("%s", YAHOO.example.onMenuBarReady);
    </script>
    '''%(self.root.title,self.root.title)
        ]
        

def factory(blog):
    return YahooMenuTool(blog)
