from chii import command

@command('lambda')
def lambda_command(self, nick, host, channel, *args):
    """.lambda <command_name>: <anonymous function body> (note: passed nick, host, channel, *args)"""
    # handle new lambda function creation
    if not len(args) > 1 or not args[0].endswith(':'):
        return 'check the help yo'

    cmd_name, args = args[0][:-1], args[1:]
    if cmd_name in self.commands:
        if hasattr(self.commands[cmd_name], '_registry'):
            return "lambda commands can't override normal commands"
    try:
        command = eval(' '.join(('lambda nick, host, channel, *args:',) + args))
    except Exception as e:
        return 'not a valid lambda function: %s' % e
    command.__doc__ = "lambda function added by \002%s\002. lambda nick, host, channel, *args: \002%s" % (nick, ' '.join(args))
    command._restrict = None
    self.commands[cmd_name] = command
    return 'added new lambda function to commands as %s' % cmd_name
