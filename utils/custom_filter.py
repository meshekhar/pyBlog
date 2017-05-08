'''
Created on Apr 29, 2017

@author: ravi
'''
import re
from jinja2 import evalcontextfilter, Markup, escape

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@evalcontextfilter
def nl2br(eval_ctx, value):
    """
    Example filter that breaks a text into HTML line 
    breaks and paragraphs and marks the return value 
    as safe HTML string if autoescaping is enabled:
    """
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', Markup('<br>\n'))
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result