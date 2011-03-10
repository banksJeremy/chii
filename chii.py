#!/usr/bin/env python

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

import new, os, sys, time
import yaml

config_file = 'bot.config'

if os.path.isfile(config_file):
    with open(config_file) as f:
        config = yaml.load(f.read())
else:
    print 'Missing configuration file!'
    sys.exit(0)

def register(f):
    """Decorator that marks a function as a bot command"""
    f._registered = True
    f._registered_name = f.__name__
    f._admin_only = False
    return f

def alias(*args):
    """Decorator that assigns a list of aliases to a botcommand"""
    def decorator(f):
        f._aliases = list(args)
        return f
    return decorator

def admin(f):
    def wrapper(self, nick, host, *args):
        if '!'.join((nick, host)) in self.chii.admins:
            return f(self, nick, host, *args)
        else:
            return '\002denied !!\002 shit, cat'
    wrapper.__doc__ = f.__doc__
    wrapper._registered = True
    wrapper._registered_name = f.__name__
    wrapper._admin_only = True
    return wrapper

class Logger:
    """A simple logger class"""
    def __init__(self):
        self.file = open(config['logfile'], 'a')

    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()


class Registry:
    """A class that tracks modules for command, etc"""
    def __init__(self, chii):
        self.chii = chii
        self.registry = {}

    def add_to_registry(self, method):
        names = [method._registered_name]
        if hasattr(method, '_aliases'):
            names = names + method._aliases
        for name in names:
            if name in self.registry:
                print 'Warning! Registry already contains %s' % name    
            self.registry[name] = new.instancemethod(method, self, Registry)

    def update_registry(self, path):
        def add_methods(package, modules):
            sys.path.append(os.path.dirname(path))
            for module in modules:
                try:
                    mod = __import__('%s.%s' % (package, module), globals(), locals(), [module], -1)
                except Exception as e:
                    print 'Error importing %s: %s' % (module, e)
                    break
                registered = filter(lambda x: hasattr(x, '_registered'), (getattr(mod, x) for x in dir(mod) if not x.startswith('_')))
                for method in registered:
                    self.add_to_registry(method)

        def reload_modules(package, modules):
            pkg = __import__(package)
            for module in modules:
                if hasattr(pkg, module):
                    mod = getattr(pkg, module)
                    for attr in [x for x in dir(mod) if not x.startswith('_')]:
                        delattr(mod, attr)
                    reload(sys.modules['%s.%s' % (package, module)])

        path = os.path.abspath(path)
        package = os.path.split(path)[-1]
        modules = [f.replace('.py', '') for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py']
        # check if we're already loaded
        if self.registry:
            self.registry = {}
            reload_modules(package, modules)
        add_methods(package, modules)
        print 'Registering: %s' % ' '.join(sorted(self.registry.keys()))

class Chii(irc.IRCClient):
    """An IRC Bot."""

    # setup sensible defaults
    channels = config.get('channels', ['chiisadventure'])
    nickname = config.get('nickname', 'chii')
    realname = config.get('realname', 'chii')
    identpass = config.get('identpass', None)
    logging = config.get('logging', True)
    admins = config.get('admins', None)
    cmd_prefix = config.get('cmd_prefix', '.')
    cmd_path = config.get('cmd_path', 'modules/commands')
    logger = Logger()

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

        # setup bot
        self.logger.log("[connected at %s]" % time.asctime(time.localtime(time.time())))
        self.commands = Registry(self)
        self.commands.update_registry(self.cmd_path)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % time.asctime(time.localtime(time.time())))
        self.logger.close()

    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.setNick(self.nickname)
        if self.identpass:
            self.msg('nickserv', 'identify %s' % self.identpass)
        for channel in self.channels:
            self.join(channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        nick, host = user.split('!')
        self.logger.log("<%s> %s" % (nick, msg))
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            pass

        # Check if we're getting a command
        if msg.startswith(self.cmd_prefix):
            msg = msg.split()
            command, args = msg[0][1:], []
            if len(msg) > 1:
                args = msg[1:]
            if self.commands.registry.get(command, None):
                try:
                    response = self.commands.registry[command](nick, host, channel, *args)
                except Exception as e:
                    response = 'ur shit am fuked! %s' % e
                if response:
                    self.msg(channel, response)
                    self.logger.log("<%s> %s" % (self.nickname, response))

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))

    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '`'

    def irc_ERR_NICKNAMEINUSE(self, prefix, params):
        """
        Called when we try to register or change to a nickname that is already
        taken.
        """
        if self.identpass:
            self.msg('nickserv', 'ghost %s %s' % (self.nickname, self.identpass))
            reactor.callLater(4, self.setNick(self.nickname))
        else:
            self.setNick(alterCollidedNick(self._attemptedNick))



class ChiiFactory(protocol.ClientFactory):
    """A factory for ChiiBots.

    A new protocol instance will be created each time we connect to the server.
    """

    # the class of the protocol to build when new connection is made
    protocol = Chii

    def __init__(self, config):
        self.config = config

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)
    
    # create factory protocol and application
    factory = ChiiFactory(config)

    # connect factory to this host and port
    if config['ssl'] is True:
        from twisted.internet import ssl
        contextFactory = ssl.ClientContextFactory()
        reactor.connectSSL(config['server'], config['port'], factory, contextFactory)
    else:
        reactor.connectTCP(config['server'], config['port'], factory)

    # run bot
    reactor.run()
