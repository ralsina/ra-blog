# -*- coding: utf-8 -*-

import BartleBlog.backend.dbclasses as db
import BartleBlog.backend.config as config
import datetime

class Mootools:
    def __init__(self,blog):
        self.blog=blog

    def head(self):
        return ['<link rel="stylesheet" type="text/css" href="%s">'%self.blog.macros.absoluteUrl('static/css/moomenu.css'),
        '<script type="text/javascript" charset="utf-8" src="%s" ></script>'%self.blog.macros.absoluteUrl('static/js/mootools.js')]

    def gen(self, item):
        if item[1]=='home':
            c='<a href="%s">%s</a>'%(self.blog.basepath, item[0])
        elif item[1]=='archives':
            c='%s'%item[0]
        elif item[1]=='tag list':
            c='<a href="%s">%s</a>'%(self.blog.macros.absoluteUrl('categories/index.html'), item[0])
        elif item[1]=='label':
            c=item[0]
        elif item[1]=='link':
            c='<a href="%s">%s</a>'%(item[2], item[0])
        elif item[1]=='story':
            c='<a href="%s">%s</a>'%(self.blog.macros.absoluteUrl('stories/%s.html'%item[2]), item[0])
        elif item[1]=='tag':
            c='<a href="%s">%s</a>'%(self.blog.macros.absoluteUrl('categories/%s.html'%item[2].lower()), item[0])
            
        if len(item)>3 and item[3]:
            inner='\n'.join([ '<li>%s'%self.gen(i) for i in item[3]])
            return '<div class="menuHeader2">%s</div><ul class="menuSlider">%s</ul>'%(c,inner)
        else:
            return '<div class="menuHeader">%s</div>'%c
            

    def menu(self):
        self.menudata=config.getValue('blog', 'menu', config.defaultMenu)
        data='<div id=moomenu>'
        for item in self.menudata:
            if item[1]=='tag list':
                for tag in db.Category.select(orderBy=db.Category.q.name):
                    item[3].append([tag.name,'link',
                                    self.blog.macros.absoluteUrl('categories/%s.html'%tag.name.lower())])

            elif item[1]=='archives':
                plist=db.Post.select(orderBy=db.Post.q.pubDate)
                if plist.count():
                    start=plist[0].pubDate.year
                    end=plist[-1].pubDate.year
                else:
                    start=datetime.datetime.today().year
                    end=datetime.datetime.today().year
                item[3]=[]
                for year in range(start,end+1):
                    item[3].append([str(year),'link',
                                    self.blog.macros.absoluteUrl('weblog/%d/index.html'%year)])

            data+=self.gen(item)
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
