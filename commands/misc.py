import json, random, os, urllib, urllib2
from chii import config, command

IMGUR_API_KEY = config['imgur_api_key']

def get_random(items):
    index = int(random.random() * len(items))
    return items[index]

@command
def face(self, nick, host, channel, *args):
    """you need help with your face?"""
    if args:
        args = ' '.join(args).split('+')
        name = args[0].strip()
        if len(args) > 1:
            madeof = ' and '.join(x.strip() for x in args[1:])
            return "hahaha %s's face is made of %s" % (name, madeof)
        return "hahah %s's face" % name
    return 'hahah your face'

@command
def sheen(self, nick, host, channel, *args):
    """well why not"""
    return '\002I GOT TIGER BLOOD IN ME %s' % nick.upper()

@command
def neoblaze(self, nick, host, channel, *args):
    """well why not"""
    for i in range( int(random.random()*5) ):
        self.msg(channel, 'np: Pendulum - Propane Nightmares (5:13)')
    for i in range( int(random.random()*10) ):
        self.msg(channel, 'DUDU'*int(random.random()*20))

@command
def lambchops(self, nick, host, channel, *args):
    """THIS IS THE..."""
    SONG_THAT_NEVER_ENDS = [
        "THIS IS THE SONG THAT DOESN'T END",
        "YES IT GOES ON AND ON MY FRIEND",
        "SOME PEOPLE STARTED SINGING IT NOT KNOWING WHAT IT WAS",
        "AND THEY'LL CONTINUE SINGING IT FOREVER JUST BECAUSE"
    ]
    for line in SONG_THAT_NEVER_ENDS:
        self.msg(channel, line)

@command
def pat(self, nick, host, channel, *args):
    """because i am a good bot!"""
    if host.endswith('vf.shawcable.net'):
        pats = 'pat ' * int(random.random()*5)
        self.me(channel, pats + nick)
    else:
        self.me(channel, 'leg twitches, and looks at you happily')

@command
def last(self, nick, host, channel, *args):
    """that last bit was quite funny!"""
    def get_line(f, size):
        while True:
            size -= 1
            f.seek(size)
            line = f.read()
            if line.startswith('\n'):
                return f, size, line

    if self.config['log_channels']:
        log_file = os.path.join(self.config['logs_dir'], channel[1:] + '.log')
        size = os.path.getsize(log_file) - 2 # skip last \n hopefully
        with open(log_file) as f:
            last = get_line(f, size) # find last line
            line = get_line(last[0], last[1])[2].split('\n')[1].split(']', 1)[1] # get line before and clean it up!
        self.topic(channel, line.strip())
    else:
        return 'not logging, I have no fucking clue what happened 2 seconds ago'

@command
def halp(self, nick, host, channel, *args):
    """bunny said ^"""
    return 'halp halp halp!'

@command
def haha(self, nick, host, channel, *args):
    """sometimes i get giggly"""
    laughter = [
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
    ]
    haha = 'haha'
    if args:
        haha = ''.join([get_random(laughter) for x in range(len(''.join(args)))])
    return haha

@command
def bonghits(self, nick, host, channel, *args):
    """what? huh? sorry i'm a little high"""
    interjections = ['\002cough\002', '...', 'hehe', '    mmm', 'hahah',
                     '\002inhaling\002', '\002random noises\002', 'hey man',
                     'uh...', 'what? yeah...', 'haahAHHA', 'eeek', 'fuck']

    speech = []
    for word in args:
        speech.append(word)
        if int(random.random()*10) > 5:
            speech.append(get_random(interjections))
    return ' '.join(speech)




@command
def directions(self, nick, host, channel, *args):
    """try from -> to, now get lost"""
    url = 'http://www.mapquest.com/?le=t&q1=%s&q2=%s&maptype=map&vs=directions'
    if '->' not in args:
        return 'um try again'
    directions = (urllib.quote(x) for x in ' '.join(args).split('->'))
    return url % tuple(directions)


if IMGUR_API_KEY:
    @command
    def imgur(self, nick, host, channel, *args):
        """<densy> this mode is full of fail"""
        url = 'http://api.imgur.com/2/stats.json'
        request = urllib2.Request(url, None, {'key': IMGUR_API_KEY})
        response = urllib2.urlopen(request)
        results = json.load(response)['stats']['most_popular_images']
        result = get_random(results)
        return 'densy recommended. doctor approved: http://imgur.com/%s' % str(result)
