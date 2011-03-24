import json, random, os, urllib, urllib2
from chii import config, command

IMGUR_API_KEY = config['imgur_api_key']

def get_random(items):
    index = int(random.random() * len(items))
    return items[index]

@command
def face(self, channel, nick, host, *args):
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
def lambchops(self, channel, nick, host, *args):
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
def last(self, channel, nick, host, *args):
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
def directions(self, channel, nick, host, *args):
    """try from -> to, now get lost"""
    url = 'http://www.mapquest.com/?le=t&q1=%s&q2=%s&maptype=map&vs=directions'
    if '->' not in args:
        return 'um try again'
    directions = (urllib.quote(x) for x in ' '.join(args).split('->'))
    return url % tuple(directions)

if IMGUR_API_KEY:
    @command
    def imgur(self, channel, nick, host, *args):
        """<densy> this mode is full of fail"""
        url = 'http://api.imgur.com/2/stats.json'
        request = urllib2.Request(url, None, {'key': IMGUR_API_KEY})
        response = urllib2.urlopen(request)
        results = json.load(response)['stats']['most_popular_images']
        result = get_random(results)
        return 'densy recommended. doctor approved: http://imgur.com/%s' % str(result)
