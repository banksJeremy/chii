from chii import command, config, event
import random, urllib, yaml, json

PERSIST = config['lambda_persist']
SAVED_LAMBDAS = config['lambdas']

# block dangerous stuff:
DANGEROUS = (execfile, file, open, __import__, __file__, __builtins__, __package__, __name__, locals, vars, globals, input, raw_input)
for x in DANGEROUS:
    x = None

def build_lambda(args):
    """Returns name and lambda function as strings"""
    name, body = ' '.join(args).split(':', 1)
    if name.endswith(')'):
        name, args = name[:-1].split('(', 1)
    else:
        args = '*args'
    func_s = 'lambda nick, host, channel, %s: %s' % (args, body)
    return func_s, name

@command('lambda', 'def')
def lambda_command(self, nick, host, channel, *args):
    """add new functions to the bot using python lambda functions"""
    def list_lambda(nick, args):
        lambdas = self.config['lambdas']
        if lambdas:
            return 'lambdas: %s' % ' '.join(x for x in self.config['lambdas'])
        else:
            return 'no lambdas found'

    def del_lambda(nick, args):
        name = args[0]
        del self.config[lambdas][name]        
        return 'deleted %s' % name

    def add_lambda(nick, args):
        # build lambda, command name from args
        func_s, name = build_lambda(args)
        # return if command by that name exists
        if name in self.commands:
            if hasattr(self.commands[name], '_registry'):
                return "lambda commands can't override normal commands"
        # try to eval our lambda function
        try:
            func = eval(func_s)
        except Exception as e:
            return 'not a valid lambda function: %s' % e
        # save to config if persist_lambda is on
        if PERSIST:
            if not SAVED_LAMBDAS:
                self.config['lambdas'] = {}
            self.config['lambdas'][name] = [func_s, nick]
            self.config.save()
        # build wrapper for our lambda
        def lambda_wrapper(nick, host, channel, *args):
            try:
                args = eval(' '.join(args) + ',')
            except:
                pass
            return str(func(nick, host, channel, *args))
        # save lambda command into our command registry
        lambda_wrapper.__doc__ = "lambda function added by \002%s\002. %s" % (nick, func_s)
        lambda_wrapper._restrict = None
        self.commands[name] = lambda_wrapper
        return 'added new lambda function to commands as %s' % name

    dispatch = {
        (lambda x: not x)(args): list_lambda,
        (lambda x: x and x[0].endswith(':'))(args): add_lambda,
        (lambda x: x and x[0] == 'del')(args): del_lambda,
    }

    return dispatch[True](nick, args)

if PERSIST and SAVED_LAMBDAS:
    @event('load')
    def load_lambdas(self, *args):
        for name in SAVED_LAMBDAS.keys():
            # build lambda, command name from args
            func_s, nick = self.config['lambdas'][name]
            # return if command by that name exists
            if name in self.commands:
                if hasattr(self.commands[name], '_registry'):
                    print "lambda commands can't override normal commands"
                    break
            # try to eval our lambda function
            try:
                func = eval(func_s)
            except Exception as e:
                print 'not a valid lambda function: %s' % e
                break
            # build wrapper for our lambda
            def lambda_wrapper(nick, host, channel, *args):
                try:
                    args = eval(' '.join(args) + ',') 
                except:
                    pass
                return str(func(nick, host, channel, *args))
            # save lambda command into our command registry
            lambda_wrapper.__doc__ = "lambda function added by \002%s\002. %s" % (nick, func_s)
            lambda_wrapper._restrict = None
            self.commands[name] = lambda_wrapper
            print 'added new lambda function to commands as %s' % name
