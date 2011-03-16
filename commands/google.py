import json, urllib, urllib2, re, sys
from chii import command, config

GOOGLE_API_KEY = config['google_api_key']

if GOOGLE_API_KEY:
    MY_IP = urllib.urlopen('http://www.whatismyip.com/automation/n09230945.asp').read()
    YOUTUBE_PATTERN = re.compile('(http://www.youtube.com[^\&]+)')
    SEARCH_API = (
        {'url': 'web', 'aliases': ('g', 'google')},
        {'url': 'books', 'aliases': ('gb', 'books')},
        {'url': 'images', 'aliases': ('gi', 'images')},
        {'url': 'patents', 'aliases': ('gp', 'patents')},
        {'url': 'video', 'aliases': ('yt', 'youtube')},
    )

    def build_search(api):
        @command(*api['aliases'])
        def search(self, nick, host, channel, *args):
            if args:
                query = '%20'.join(args)
            else:
                return 'you require a query'
            url = 'https://ajax.googleapis.com/ajax/services/search/%s?v=1.0&q=%s&key=%s&userip=%s' % (api['url'], query, GOOGLE_API_KEY, MY_IP)
            request = urllib2.Request(url, None, {'Referer': 'http://quoth.notune.com'})
            response = urllib2.urlopen(request)
            result = json.load(response)['responseData']['results'][0]
            title, url = result['titleNoFormatting'], result['url']
            msg = 'top result: %s - %s' % (title, url)
            return str(msg)
        search.__doc__ = "searches %s" % api['url']
        return search

    for api in SEARCH_API:
        setattr(sys.modules[__name__], api['url'], build_search(api))

    @command('yt', 'youtube')
    def youtube_search(*args):
        """search youtube"""
        msg, url = video(*args).rsplit(' ', 1)
        url = url.replace('%3F', '?').replace('%3D', '=')
        if 'youtube' in url:
            url = re.search(YOUTUBE_PATTERN, url).group()
        return ' '.join((msg, url))

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
        return json.load(response)['responseData']['translatedText']
