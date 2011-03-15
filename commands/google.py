import json, urllib, urllib2, re
from chii import command, config

GOOGLE_API_KEY = config['google_api_key']

if GOOGLE_API_KEY:
    MY_IP = urllib.urlopen('http://www.whatismyip.com/automation/n09230945.asp').read()
    YOUTUBE_PATTERN = re.compile('(http://www.youtube.com[^\&]+)')
    
    @command('g', 'google')
    def google(self, nick, host, channel, *args):
        """despite its name, this actually googles for stuff!"""
        if args:
            query = '%20'.join(args)
        else:
            return 'u need a query'
        url = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&key=%s&userip=%s' % (query, GOOGLE_API_KEY, MY_IP)
        request = urllib2.Request(url, None, {'Referer': 'http://quoth.notune.com'})
        response = urllib2.urlopen(request)
        result = json.load(response)['responseData']['results'][0]
        msg = 'top result: %s - %s' % (title, url)
        return str(msg)

    @command('gb', 'books')
    def google_books(self, nick, host, channel, *args):
        """searches for books"""
        if args:
            query = '%20'.join(args)
        else:
            return 'u need a query'
        url = 'https://ajax.googleapis.com/ajax/services/search/books?v=1.0&q=%s&key=%s&userip=%s' % (query, GOOGLE_API_KEY, MY_IP)
        request = urllib2.Request(url, None, {'Referer': 'http://quoth.notune.com'})
        response = urllib2.urlopen(request)
        result = json.load(response)['responseData']['results'][0]
        msg = 'top result: %s - %s' % (title, url)
        return str(msg)

    @command('gi', 'images')
    def google_image(self, nick, host, channel, *args):
        """searches for images"""
        if args:
            query = '%20'.join(args)
        else:
            return 'u need a query'
        url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=%s&key=%s&userip=%s' % (query, GOOGLE_API_KEY, MY_IP)
        request = urllib2.Request(url, None, {'Referer': 'http://quoth.notune.com'})
        response = urllib2.urlopen(request)
        result = json.load(response)['responseData']['results'][0]
        msg = 'top result: %s - %s' % (title, url)
        return str(msg)
   
    @command('gp', 'patents')
    def google_patent(self, nick, host, channel, *args):
        """searches patents"""
        if args:
            query = '%20'.join(args)
        else:
            return 'u need a query'
        url = 'https://ajax.googleapis.com/ajax/services/search/patent?v=1.0&q=%s&key=%s&userip=%s' % (query, GOOGLE_API_KEY, MY_IP)
        request = urllib2.Request(url, None, {'Referer': 'http://quoth.notune.com'})
        response = urllib2.urlopen(request)
        result = json.load(response)['responseData']['results'][0]
        msg = 'top result: %s - %s' % (title, url)
        return str(msg)

    @command('youtube', 'yt')
    def google_video(self, nick, host, channel, *args):
        """searches for videos"""
        if args:
            query = '%20'.join(args)
        else:
            return 'u need a query'
        url = 'https://ajax.googleapis.com/ajax/services/search/video?v=1.0&q=%s&key=%s&userip=%s' % (query, GOOGLE_API_KEY, MY_IP)
        request = urllib2.Request(url, None, {'Referer': 'http://quoth.notune.com'})
        response = urllib2.urlopen(request)
        results = json.load(response)['responseData']['results']
        title, url = results[0]['titleNoFormatting'], results[0]['url']
        if 'youtube' in url:
            url = re.search(YOUTUBE_PATTERN, url).group()
            url = url.replace('%3F', '?').replace('%3D', '=')
        msg = 'top result: %s - %s' % (title, url)
        return str(msg)

    @command('gt', 'translate')
    def google_translate(self, nick, host, channel, language_pair=None, *args):
        """so kawaii"""
        if not args or not language_pair:
            return 'u need something to translate!'

        language_pair = '%7C'.join(language_pair.split('->'))
        query = '%20'.join(args)

        url = 'https://ajax.googleapis.com/ajax/services/language/translate?v=1.0&q=%s&langpair=%s' % (query, language_pair)
        request = urllib2.Request(url, None, {'Referer': 'http://quoth.notune.com'})
        response = urllib2.urlopen(request)
        results = json.load(response)['responseData']['translatedText']
        return str(results)
