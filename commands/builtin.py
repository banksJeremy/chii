from chii import register, admin

@admin
def rehash(self, nick, host, *args):
    """u don't know me"""
    self.update_registry(self.chii.cmd_path)
    return '\002rehash !!\002 rehashed'

@register
def help(self, nick, host, channel, command=None, *args):
    """returns help nogga"""
    available_help = self.registry.keys()
    if '!'.join((nick, host)) not in self.chii.admins:
        available_help = filter(lambda x: not self.registry[x]._admin_only, available_help)

    if command in available_help:
        method = self.registry[command]
        if method.__doc__:
            help_msg = method.__doc__.strip().split('\n')[0]
            return '\002help ?? %s\002 >> %s' % (command, help_msg)
        return '\002help ??\002 eh wut'
    return '\002help ?? available commands\002 >> %s' % ', '.join(sorted(available_help))

@register
def say(self, nick, host, channel, *args):
    """SAY SMTH ELSE"""
    self.chii.msg(channel, ' '.join(args))

@register
def me(self, nick, host, channel, *args):
    """strike a pose"""
    self.chii.me(channel, ' '.join(args))

@register
def topic(self, nick, host, channel, *args):
    """how 2 make babby"""
    self.chii.topic(channel, ' '.join(args))

@admin
def mode(self, nick, host, channel, *args):
    """change the game"""
    new_mode = 'MODE %s' % ' '.join(args)
    self.chii.sendLine(new_mode)

def op(self): pass

def deop(self): pass

def voice(self): pass

def devoice(self): pass
