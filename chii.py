#!/usr/bin/env python

import argparse, new, os, sys, time, traceback
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, defer
from twisted.python import log
import yaml

CONFIG_FILE = 'bot.config'

EVENT_TYPES = (
    'msg',
    'privmsg',
    'pubmsg',
    'join',
    'kick',
)

config = {}
if os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE) as f:
        config = yaml.load(f.read())

def command(*args, **kwargs):
    """Decorator which adds callable to command registry"""
    if args and not hasattr(args[0], '__call__') or kwargs:
        # decorator used with args for aliases or keyward arg
        def decorator(func):
            def wrapper(*func_args, **func_kwargs):
                return func(*func_args, **func_kwargs)
            wrapper._registry = 'commands'
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            if args:
                wrapper._command_names = (func.__name__,) + args
            else:
                # used with keyword arg but not alias names!
                wrapper._command_names = (func.__name__,)
            if 'restrict' in kwargs:
                wrapper._restrict = kwargs['restrict']
            else:
                wrapper._restrict = None
            return wrapper
        return decorator
    
    else:
        # used without any args
        func = args[0]
        def wrapper(*func_args, **func_kwargs):
            return func(*func_args, **func_kwargs)
        wrapper._registry = 'commands'
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper._command_names = (func.__name__,)
        if 'restrict' in kwargs:
            wrapper._restrict = kwargs['restrict']
        else:
            wrapper._restrict = None
        return wrapper

def event(event_type):
    """Decorator which adds callable to the event registry"""
    def decorator(func):
        def wrapper(*func_args, **func_kwargs):
            return func(*func_args, **func_kwargs)
        if event_type in EVENT_TYPES:
            wrapper._registry = 'events'
            wrapper._event_type = event_type
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator

def task(*args):
    """Decorator which adds callable to task registry"""
    def decorator(func):
        def wrapper(*func_args, **func_kwargs):
            return func(*func_args, **func_kwargs)
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper._registry = 'tasks'
        wrapper._task_interval = args[0]
        return wrapper
    return decorator

    
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
        self.commands = {}
        self.events = {k: [] for k in (EVENT_TYPES)}
        self.tasks = []
        self._initialized = False

    def update_registry(self, paths):
        def add_to_registry(package, modules):
            def add_command(method):
                for name in method._command_names:
                    if name in self.commands:
                        print 'Warning! commands registry already contains %s' % name
                    self.commands[name] = new.instancemethod(method, self, Registry)
                    print '[command] %s' % name
        
            def add_event(method):
                if method._event_type in EVENT_TYPES:
                    self.events[method._event_type].append(new.instancemethod(method, self, Registry))
                    print '[event - %s] %s ' % (method._event_type, method.__name__)
        
            def add_task(method):
                self.tasks.append(new.instancemethod(method, self, Registry))
                print '[task - %s] %s' % (method._task_interval, method.__name__)

            def error(method):
                print 'Eh, wut?'

            dispatch = {'commands': add_command, 'events': add_event, 'tasks': add_task}

            for module in modules:
                try:
                    print 'Importing', module
                    mod = __import__('%s.%s' % (package, module), globals(), locals(), [module], -1)
                except Exception as e:
                    print 'Error importing %s', module
                    traceback.print_exc()
                    break
                registered = filter(lambda x: hasattr(x, '_registry'), (getattr(mod, x) for x in dir(mod) if not x.startswith('_')))
                for method in registered:
                    dispatch.get(method._registry, error)(method)

        def reload_modules(package, modules):
            pkg = __import__(package)
            for module in modules:
                if hasattr(pkg, module):
                    mod = getattr(pkg, module)
                    for attr in [x for x in dir(mod) if not x.startswith('_')]:
                        delattr(mod, attr)
                    reload(sys.modules['%s.%s' % (package, module)])

        if paths:
            for path in paths:
                print 'Looking in %s for registered callables...' % path
                path = os.path.abspath(path)
                package = os.path.split(path)[-1]
                modules = [f.replace('.py', '') for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py']
                # check if we're already loaded
                if self._initialized:
                    reload_modules(package, modules)
                else:
                    self._initialized = True
                add_to_registry(package, modules)


class Chii:
    """Class that handles all the chii specific functionality"""
    def _handle_command(self, channel, nick, host, msg):
        """Handles commands, passing them proper args, etc"""
        def check_permission(restrict_to, nick, host):
            if restrict_to is None:
                return True
            for member in (nick, host, '!'.join((nick, host))):
                if member in config['user_roles'][restrict_to]:
                    return True
            return False
        
        msg = msg.split()
        command, args = msg[0][1:], []
        command = self.registry.commands.get(command, None)
        if command:
            if check_permission(command._restrict, nick, host):
                if len(msg) > 1:
                    args = msg[1:]
                try:
                    response = command(nick, host, channel, *args)
                except Exception as e:
                    response = 'ur shit am fuked! %s' % e
                    traceback.print_exc()
                if response:
                    self.msg(channel, response)
                    self.logger.log("<%s> %s" % (self.nickname, response))


    def _handle_event(self, event_type, channel, *args, **kwargs):
        """Handles event and catches errors, returns result of event as bot message"""
        for func in self.registry.events[event_type]:
            try:
                response = func(channel, *args, **kwargs)
            except Exception as e:
                    response = 'ur shit am fuked! %s' % e
                    traceback.print_exc()
            if response:
                self.msg(channel, response)
                self.logger.log("<%s> %s" % (self.nickname, response))


class ChiiBot(irc.IRCClient, Chii):
    # setup sensible defaults
    channels = config.get('channels', ['chiisadventure'])
    nickname = config.get('nickname', 'chii')
    realname = config.get('realname', 'chii')
    identpass = config.get('identpass', None)
    logging = config.get('logging', True)
    admins = config.get('admins', None)
    cmd_prefix = config.get('cmd_prefix', '.')
    logger = Logger()

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

        # setup bot
        self.logger.log("[connected at %s]" % time.asctime(time.localtime(time.time())))
        self.registry = Registry(self)
        self.registry.update_registry(config.get('modules', None))

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

        # catch-all msg event
        self._handle_event('msg', channel, nick, host, msg)

        if channel == self.nickname:
            # this is a message from a user
            self._handle_event('privmsg', channel, nick, host, msg)
        else:
            # this is a message in the channel
            self._handle_event('pubmsg', channel, nick, host, msg)

        # Check if we're getting a command
        if msg.startswith(self.cmd_prefix):
            self._handle_command(channel, nick, host, msg)

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
            self.setNick(self.nickname)
        else:
            self.setNick(alterCollidedNick(self._attemptedNick))

class ChiiFactory(protocol.ClientFactory):
    """A factory for ChiiBots.

    A new protocol instance will be created each time we connect to the server.
    """

    # the class of the protocol to build when new connection is made
    protocol = ChiiBot

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
