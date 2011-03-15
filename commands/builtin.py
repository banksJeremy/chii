from chii import check_permission, command

@command(restrict='admins')
def rehash(self, nick, host, channel, *args):
    """u don't know me"""
    self.update_registry()
    return '\002rehash !!\002 rehashed'

@command
def help(self, nick, host, channel, command=None, *args):
    """returns help nogga"""
    commands = filter(lambda x: self.commands[x]._restrict is None, self.commands)
    for role in self.config['user_roles']:
        if check_permission(role, nick, host):
            commands.extend(filter(lambda x: self.commands[x]._restrict == role, self.commands))

    if command in commands:
        method = self.commands[command]
        if method.__doc__:
            help_msg = method.__doc__.strip().split('\n')[0]
            return '\002help ?? %s\002 >> %s' % (command, help_msg)
        return '\002help ??\002 eh wut'
    return '\002help ?? available commands\002 >> %s' % ', '.join(sorted(commands))

@command
def say(self, nick, host, channel, *args):
    """SAY SMTH ELSE"""
    self.msg(channel, ' '.join(args))

@command
def me(self, nick, host, channel, *args):
    """strike a pose"""
    self.me(channel, ' '.join(args))

@command
def topic(self, nick, host, channel, *args):
    """how 2 make babby"""
    self.topic(channel, ' '.join(args))

@command(restrict='admins')
def mode(self, nick, host, channel, *args):
    """change the game"""
    new_mode = 'MODE %s' % ' '.join(args)
    self.sendLine(new_mode)

def op(self): pass

def deop(self): pass

def voice(self): pass

def devoice(self): pass
