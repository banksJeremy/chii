from chii import event

@event('action')
def haha(self, nick, host, channel, action):
    if 'trout' in action:
        self.me(channel, 'slaps %s around with a large carp' % nick)

@event('msg')
def haha(self, nick, host, channel, msg):
    if (msg.startswith('who is') or msg.startswith('who the')) and (msg.endswith('best?') or msg.endswith('best')):
        if self.config['owner'] in '!'.join((nick, host)):
            if msg.startswith('who the'):
                response = "%s's the best!" % nick
            else:
                response = '%s is the %s best!' % (nick, ' '.join(msg.split()[2:-1]))
        else:
            response = 'not you'
        if self.nickname == channel:
            self.msg(nick, response)
        else:
            self.msg(channel, response)
