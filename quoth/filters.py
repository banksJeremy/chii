import re

_nick_re = re.compile(r'([\[<][\w@]+[\]>])[^\[<]')

def reformat_quote(quote):
    def repl_nick(match):
        return match.group().replace('@', '').replace('[', '<').replace(']', '>')
    return re.sub(_nick_re, repl_nick, quote)
