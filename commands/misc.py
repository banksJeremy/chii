import json, random, os, urllib, urllib2
from chii import config, command

IMGUR_API_KEY = config.get('imgur_api_key', None)

def get_random(items):
    index = int(random.random() * len(items))
    return items[index]

@command
def face(self, nick, host, channel, *args):
    """you need help with your face?"""
    if args:
        madeof = [x[1:] for x in args if x.startswith('+')]
        name = ' '.join([x for x in args if not x.startswith('+')])
        if madeof:
            madeof = ' and '.join(madeof)
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
        self.chii.msg(channel, 'np: Pendulum - Propane Nightmares (5:13)')
    for i in range( int(random.random()*10) ):
        self.chii.msg(channel, 'DUDU'*int(random.random()*20))

@command
def pat(self, nick, host, channel, *args):
    """because i am a good bot!"""
    if host.endswith('vf.shawcable.net'):
        pats = 'pat ' * int(random.random()*5)
        self.chii.me(channel, pats + nick)
    else:
        self.chii.me(channel, 'leg twitches, and looks at you happily')

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

    log = self.chii.config['logfile']
    size = os.path.getsize(log) - 2 # skip last \n hopefully
    with open(log) as f:
        last = get_line(f, size) # find last line
        line = get_line(last[0], last[1])[2].split('\n')[1].split(']', 1)[1] # get line before and clean it up!
    self.chii.topic(channel, line.strip())

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
        haha = ''.join([get_random(laughter) for laugh in args])
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
    command.__doc__ = "f = lambda nick, host, channel, *args: " + ' '.join(args)
    command._restrict = None
    self.commands[cmd_name] = command
    return 'added new lambda function to commands as %s' % cmd_name
