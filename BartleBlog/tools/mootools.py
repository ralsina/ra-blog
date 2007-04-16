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
        self.img=self.blog.macros.absoluteUrl('static/down.gif')
        
        s=db.Post.select(orderBy=db.Post.q.pubDate)
        years=range(s[0].pubDate.year,s[-1].pubDate.year+1)
        years=[[' '+str(y),blog.macros.absoluteUrl('weblog/%d/index.html'%y)] for y in years]

        self.menudesc=[
            ['Home',blog.macros.absoluteUrl('weblog/index.html')],
            ['Articles',blog.macros.absoluteUrl('stories/index.html')],
            ['Archives',blog.macros.absoluteUrl('weblog/archive.html')]]+years+[
            ['Software',None],
            [' RaSCAN','http://rascan.blogsite.org'],
            [' Ra-Plugins','http://raplugins.blogsite.org'],
            [' RaSPF','http://raspf.blogsite.org'],
            [' CherryTV','http://cherrytv.blogsite.org'],
            [' BartleBlog',blog.macros.absoluteUrl('categories/bartleblog.html')],
            ['Tags',blog.macros.absoluteUrl('categories/index.html')]
            ]
        for tag in db.Category.select():
            self.menudesc.append([' '+tag.name,blog.macros.absoluteUrl('categories/%s.html'%tag.name.lower())])

        curDepth=0
        self.root=menuitem(None,["menubar",None],0,self.img)
        curItem=self.root
        for line in self.menudesc:
            d=linedepth(line[0])
            curItem=self.root
            for x in range(0,d):
                curItem=curItem.children[-1]
            menuitem(curItem,line,d+1,self.img)


    def head(self):
        return ['<link rel="stylesheet" type="text/css" href="%s">'%self.blog.macros.absoluteUrl('static/css/moomenu.css'),
        '<script type="text/javascript" charset="utf-8" src="%s" ></script>'%self.blog.macros.absoluteUrl('static/js/mootools.js')]

        
    def menu(self):
        return str(self.root)
        
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
