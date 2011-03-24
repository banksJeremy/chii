import os, random, re
from chii import event

from megahal import *

BRAIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'megahal.brain')
CHATTINESS = 0

megahal = MegaHAL(brainfile=BRAIN, order=DEFAULT_ORDER, timeout=DEFAULT_TIMEOUT)

@event('msg')
def megachat(self, channel, nick, host, msg):
    if self.nickname.lower() in msg.lower():
        msg = re.compile(self.nickname + "[:,]* ?", re.I).sub('', msg)
        prefix = "%s: " % nick
    else:
        prefix = ''

    if prefix or random.random() <= CHATTINESS:
        return prefix + megahal.get_reply(msg)

    megahal.learn(msg)
    megahal.sync()
