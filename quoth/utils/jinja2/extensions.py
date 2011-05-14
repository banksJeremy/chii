from jinja2 import nodes
from jinja2.ext import Extension
from django.conf import settings

class StaticURLExtension(Extension):
    tags = set(['static_url'])

    def parse(self, parser):
        token = parser.stream.next()
        bits = []
        while not parser.stream.current.type == 'block_end':
            bits.append(parser.stream.next())
        asset = nodes.Const("".join([b.value for b in bits]))
        return nodes.Output([self.call_method('_static_url', args=[asset])]).set_lineno(token.lineno)

    def _static_url(self, asset):
        return ''.join([settings.STATIC_URL, asset])

# short import name
static_url = StaticURLExtension
