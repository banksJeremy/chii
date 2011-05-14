from coffin.template import Library
from jinja2.runtime import Undefined
from jinja2.filters import escape
from jinja2 import Markup
from django.template.defaultfilters import linebreaks
import re

_nick_re = re.compile(r'([\[<][\w@]+[\]>])[^\[<]')
_add_line_re = re.compile(r' [<\w]+[>] ')

register = Library()

@register.filter(jinja2_only=True)
def format_quote(value, args=None):
    def reformat_nicks(quote):
        def repl_nick(match):
            return match.group().replace('@', '').replace('[', '<').replace(']', '>')
        return re.sub(_nick_re, repl_nick, value)

    def insert_newlines(quote):
        return re.sub(_add_line_re, lambda x: '\n' + x.group(), quote)

    def newline_to_br(value):
        return value.replace('\n', '<br />')

    for f in (reformat_nicks, insert_newlines, escape, str, newline_to_br):
        value = f(value)

    return value
