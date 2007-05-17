# -*- coding: utf-8 -*-

from colubrid import RegexApplication, HttpResponse, execute
from colubrid.server import StaticExports
from colubrid.exceptions import PageNotFound
from BartleBlog.backend.blog import Blog
import BartleBlog.backend.dbclasses as db
import os, codecs, sys

class webBlog(Blog):
    def __init__(self):
        Blog.__init__(self)
        self.basepath='http://localhost:8080/'
        self.dest_dir=os.path.expanduser("~/.bartleblog/preview")
        if not os.path.isdir(self.dest_dir):
            os.mkdir(self.dest_dir)
        

class MyApplication(RegexApplication):
    blog=webBlog()
    urls = [
        ('quit', 'quit'), 
        (r'^(.*?)$', 'page'), 
        (r'^(.*?)/(.*?)$', 'page'), 
        (r'^(.*?)/(.*?)/(.*?)$', 'page'), 
        (r'^(.*?)/(.*?)/(.*?)/(.*?)$', 'page')
    ]

    def quit(self):
        sys.exit(0)

    def page(self, *args):
        path=''.join(args)
        page=db.pageByPath(path)
        self.blog.renderPage(page)
        fn=os.path.join(self.blog.dest_dir, path)
        if os.path.isfile(fn):
            resp=HttpResponse(codecs.open(fn).read())
            os.unlink(fn)
            return resp
        else:
            raise PageNotFound(path)

def run():    
    app = MyApplication
    app = StaticExports(app, {'/static': os.path.expanduser('~/.bartleblog/weblog/static')})
    execute(app)
