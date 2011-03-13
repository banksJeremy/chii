import random
from chii import event

LAUGHTER = (
        'hahah',
        'lollolol',
        'rofl',
        'aaaaaaaaaaaaaaaaa',
        'aaaahahah',
        'ahahah',
        'bahhhhhh',
        'waaaaaaaaaaah',
        'hshshshshahaah',
        'MOTHERFUCKING H & A',
        'hahahahahaahhahahaahahahahhhahhhhahahahahahahahahahahahahahahahaahahahaha',
)

def get_random(items):
    index = int(random.random() * len(items))
    return items[index]

@event('msg')
def haha(self, channel, nick, host, msg):
    if random.random() > .8:
        if 'haha' in msg.lower():
            haha = ''
            for i in range(int(random.random()*10)):
                haha += get_random(LAUGHTER)
            return haha
