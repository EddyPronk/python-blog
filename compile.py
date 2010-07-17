import markdown2
from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions
import datetime, os
from glob import glob
import hashlib
import rfc3339

def convert(content):
    def date(y,m,d):
        return datetime.date(y,m,d).strftime('%A %B %d') + ' by Eddy Pronk'
    return markdown2.markdown(content)

class Context(object):
    def vars(self, **kwargs):
        d = dict(context.__class__.__dict__)
        d.update(kwargs)
        d['datetime'] = datetime
        d['rfc3339'] = rfc3339
        return d
    def posts(): return posts2
    def feed_id(): return 'urn:uuid:cc149f90-9d99-45ab-8816-79c9893b7ca1'
    def make_id(post):
        readable = ':'.join(['http://www.muftor.com/blog/', str(post.date), post.title])
        return 'urn:sha1:' + hashlib.sha1(readable).hexdigest()
    
context = Context()
lookup = TemplateLookup(directories=['/home/epronk/blog/weblog/templates', '.'])

class Post(object) : pass

def read(path):
    content = open(path).read()
    title = os.path.split(path)[-1][11:]
    post = Post()
    post.date = datetime.datetime.strptime(os.path.split(path)[-1][:10], "%Y-%m-%d").date()
    post.title = title
    post.filename = title.replace(' ', '_').lower() + '.html'
    post.url = 'http://www.muftor.com/blog/' + post.filename
    post.content = convert(str(content))
    return post

posts2 = [ read(path) for path in glob('posts/*[!~]') ]
posts2.sort(key = lambda p: p.date, reverse=True)

def posts(): return posts2

for post in posts():
    print post.date, post.title
    mytemplate = Template(filename='templates/post.mako', lookup = lookup)
    open(os.path.join('deploy', 'blog', post.filename), 'w').write(mytemplate.render(**context.vars(post=post)))

def generate(infile, outfile, context):
    print outfile
    mytemplate = Template(filename=infile, lookup = lookup)
    try:
        open(os.path.join('deploy', 'blog', outfile), 'w').write(mytemplate.render(**context.vars()))
    except:
        print 'error'
        print exceptions.text_error_template().render()

generate('templates/foo.mako', 'index.html', context)
generate('templates/atom.mako', 'atom.xml', context)
