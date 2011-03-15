from chii import command, config, event
import random, urllib, yaml, json

PERSIST = config['lambda_persist']
SAVED_LAMBDAS = config['lambdas']

@command('lambda')
def lambda_command(self, nick, host, channel, *args):
    """.lambda <command_name>: <anonymous function body> (note: passed nick, host, channel, *args)"""
    # handle new lambda function creation
    if not len(args) > 1 or not args[0].endswith(':'):
        return 'check the help yo'

    cmd_name, args = args[0][:-1], args[1:]
    func = ' '.join(('lambda nick, host, channel, *args:',) + args)
    if cmd_name in self.commands:
        if hasattr(self.commands[cmd_name], '_registry'):
            return "lambda commands can't override normal commands"
    try:
        command = eval(func)
    except Exception as e:
        return 'not a valid lambda function: %s' % e
    if PERSIST:
        if not SAVED_LAMBDAS:
            self.config['lambdas'] = []
        self.config['lambdas'].append([cmd_name, func, nick])
        self.config.save()
    command.__doc__ = "lambda function added by \002%s\002. lambda nick, host, channel, *args: \002%s" % (nick, ' '.join(args))
    command._restrict = None
    self.commands[cmd_name] = command
    return 'added new lambda function to commands as %s' % cmd_name

if PERSIST and SAVED_LAMBDAS:
    @event('load')
    def load_lambdas(self, *args):
        for lambda_f in SAVED_LAMBDAS:
            cmd_name, func, nick = lambda_f
            try:
                command = eval(func)
            except Exception as e:
                print 'not a valid lambda function: %s' % e
            command.__doc__ = "lambda function added by \002%s\002. lambda nick, host, channel, *args: \002%s" % (nick, ' '.join(args))
            command._restrict = None
            self.commands[cmd_name] = command
            print 'Loaded lambda function %s' % cmd_name
