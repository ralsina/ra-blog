# -*- coding: utf-8 -*-

import BartleBlog.backend.dbclasses as db

def linedepth(line):
    c=0
    while line[c]==' ':
        c=c+1
    return c

class menuitem:
    def __init__(self,parent,data,depth,img):
        self.parent=parent
        self.img=img
        self.title=data[0].strip()
        if data[1]:
            self.link='<a href="%s">%s</a>'%(data[1],self.title)
        else:
            self.link=self.title
        self.children=[]
        self.depth=depth
        if parent:
            self.parent.children.append(self)

    
    def __repr__(self):
        
        if self.depth==0:
            return '''<div id="moomenu">%s</div>'''%('\n\n'.join([str(x) for x in self.children]))
        elif self.depth==1:
            if self.children:
                return '''
                <div class="menuHeader2">%s</div>
                <ul class="menuSlider">%s</ul>
                '''%(self.link,'\n\n'.join([str(x) for x in self.children]))
            else:
                return '<div class="menuHeader">%s</div>'%(self.link)
        else:
            return '''
            <li>%s</li>
            '''%self.link

class Mootools:
    def __init__(self,blog):
        self.blog=blog

    def head(self):
        return ['<link rel="stylesheet" type="text/css" href="%s">'%self.blog.macros.absoluteUrl('static/css/moomenu.css'),
        '<script type="text/javascript" charset="utf-8" src="%s" ></script>'%self.blog.macros.absoluteUrl('static/js/mootools.js')]

    def gen(self, item):
        data=''
        if item[3]:
            h='<div class="menuHeader2">'            
        else:
            h='<div class="menuHeader">'
        if item[1]=='home':
            c='<a href="%s">%s</a>'%(self.blog.basepath, item[0])
        elif item[1]=='archives':
            h='<div class="menuHeader2">' # Archives actually have a submenu
            c='<a href="%s">%s</a>'%(self.blog.basepath, item[0])
        elif item[1]=='tag list':
            h='<div class="menuHeader2">' # Tag Lists actually have a submenu
            c='<a href="%s">%s</a>'%(self.blog.basepath, item[0])
        elif item[1]=='label':
            c='<a href="%s">%s</a>'%(self.blog.basepath, item[0])
        elif item[1]=='link':
            c='<a href="%s">%s</a>'%(self.blog.basepath, item[0])
        elif item[1]=='story':
            c='<a href="%s">%s</a>'%(self.blog.basepath, item[0])
        elif item[1]=='tag':
            c='<a href="%s">%s</a>'%(self.blog.basepath, item[0])
            
        return h+c+'</div>'
            

    def menu(self):
        self.menudata=config.getValue('blog', 'menu', config.defaultMenu)
        data='<div id=moomenu>'
        for titem in self.menudata:
            data+=self.gen(titem)        
        data+='</div>'
        return data
        
    def accordionScript(self,controlClass,sliderClass):
        '''Takes as arguments the names of two CSS classes.
        
        controlClass is what you click to expand the accordion,
        sliderClass is what contains the piece that expands.
        '''
        return '''
                    <script type="text/javaScript">
                        function accordionInit() {
                                new Accordion($$('.%s'),$$('.%s'));
                        }
                        window.addEvent('domready',accordionInit);
                    </script>
        '''%(controlClass,sliderClass)
        
        
def factory (blog):
    return Mootools(blog)
