from chii import check_permission, command

import inspect

# utilities
def get_args(func):
    argspec = inspect.getargspec(fun)
    print 'args:'
    print ' '.join(argspec['args'])
    print 'kwargs:'
    print ' '.join(argspec['varargs'])
    print 'keywords:'
    print ' '.join(argspec['keywords'])
    print 'defaults:'
    print ' '.join(argspec['defaults'])

@command('exec', restrict='admins')
def evil_exec(self, nick, host, channel, *args):
    """u don't know me"""
    if args:
        from twisted.python import log
        from StringIO import StringIO

        # add twisted log observer
        output = StringIO()
        observer = log.FileLogObserver(output)
        observer.start()
        # grab initial "log started" message, we don't care about that
        output.getvalue()

        # exec args
        exec compile(' '.join(args), '', 'single')

        # stop observer and return output
        observer.stop()
        logged = output.getvalue().partition('] ')[2]
        output.close()
        return logged

@command('eval', restrict='admins')
def evil_eval(self, nick, host, channel, *args):
    """u don't know me"""
    if args:
        return str(eval(' '.join(args)))
