from chii import command, config, event
import random, urllib, yaml, json

PERSIST = config['lambda_persist']
SAVED_LAMBDAS = config['lambdas']

# block dangerous stuff:
DANGEROUS = (execfile, file, open, __import__, __file__, __builtins__, __package__, __name__, locals, vars, globals, input, raw_input)
for x in DANGEROUS:
    x = None

def build_lambda(args):
    """Returns lambda name and string of function definition"""
    name, body = ' '.join(args).split(':', 1)
    if name.endswith(')'):
        name, args = name[:-1].split('(', 1)
    else:
        args = '*args'
    definition = 'lambda nick, host, channel, %s: %s' % (args, body)
    return definition, name

@command('lambda', 'def')
def lambda_command(self, nick, host, channel, *args):
    """add new functions to the bot using python lambda functions"""
    # handle new lambda function creation
    try:
        definition, name = build_lambda(args)
        func = eval(definition)
    except Exception as e:
        return 'not a valid lambda function: %s' % e
    if name in self.commands:
        if hasattr(self.commands[name], '_registry'):
            return "lambda commands can't override normal commands"
    if PERSIST:
        if not SAVED_LAMBDAS:
            self.config['lambdas'] = {}
        self.config['lambdas'][name] = (definition, nick)
        self.config.save()
    def lambda_wrapper(nick, host, channel, *args):
        try:
            args = eval(' '.join(args) + ',')
        except:
            pass
        return str(func(nick, host, channel, *args))
    lambda_wrapper.__doc__ = "lambda function added by \002%s\002. %s" % (nick, definition)
    lambda_wrapper._restrict = None
    self.commands[name] = lambda_wrapper
    return 'added new lambda function to commands as %s' % name

if PERSIST and SAVED_LAMBDAS:
    @event('load')
    def load_lambdas(self, *args):
        for name in SAVED_LAMBDAS:
            definition, nick = SAVED_LAMBDAS[key]
            try:
                func = eval(definition)
            except Exception as e:
                print 'not a valid lambda function: %s' % e
                break
            if name in self.commands:
                if hasattr(self.commands[name], '_registry'):
                    print "lambda commands can't override normal commands"
                    break
            def lambda_wrapper(nick, host, channel, *args):
                try:
                    args = eval(' '.join(args) + ',') 
                except:
                    pass
                return str(func(nick, host, channel, *args))
            lambda_wrapper.__doc__ = "lambda function added by \002%s\002. %s" % (nick, definition)
            lambda_wrapper._restrict = None
            self.commands[name] = lambda_wrapper
            print 'added new lambda function to commands as %s' % name
