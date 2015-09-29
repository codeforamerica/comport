from jinja2 import Markup
from markdown import Markdown
md = Markdown(extensions=[])

def markdown(*args):
    return Markup(md.convert(*args))
