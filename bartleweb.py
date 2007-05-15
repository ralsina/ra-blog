from colubrid import RegexApplication, HttpResponse, execute
from colubrid.server import StaticExports
from BartleBlog.backend.blog import Blog
import BartleBlog.backend.dbclasses as db
import os, codecs

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
        (r'^(.*?)$', 'page'), 
        (r'^(.*?)/(.*?)$', 'page'), 
        (r'^(.*?)/(.*?)/(.*?)$', 'page'), 
        (r'^(.*?)/(.*?)/(.*?)/(.*?)$', 'page')
    ]

    def page(self, *args):
        path=''.join(args)
        page=db.pageByPath(path)
        self.blog.renderPage(page)
        return HttpResponse(codecs.open(os.path.join(self.blog.dest_dir, path)).read())

app = MyApplication
app = StaticExports(app, {
    '/static': './static'
})

if __name__ == '__main__':
    execute(app)
