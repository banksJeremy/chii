import json, urllib, urllib2, re
from chii import alias, config, register

GOOGLE_API_KEY = config.get('google_api_key', None)

if GOOGLE_API_KEY:
    MY_IP = urllib.urlopen('http://www.whatismyip.com/automation/n09230945.asp').read()
    YOUTUBE_PATTERN = re.compile('(http://www.youtube.com[^\&]+)')
    
    @alias('g')
    @register
    def google(self, nick, host, channel, *args):
        """despite its name, this actually googles for stuff!"""
        if args:
            query = '%20'.join(args)
        else:
            return 'u need a query'
        url = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&key=%s&userip=%s' % (query, GOOGLE_API_KEY, MY_IP)
        request = urllib2.Request(url, None, {'Referer': 'http://quoth.notune.com'})
        try:
            response = urllib2.urlopen(request)
            results = json.load(response)['responseData']['results']
            result = '%s - %s' % (results[0]['titleNoFormatting'], results[0]['url'])
            return 'top result: %s' % str(result)
        except Exception as e:
            return 'ur shit am fuked: %s' % e
    
    @alias('gi')
    @register
    def google_image(self, nick, host, channel, *args):
        """searches for images"""
        if args:
            query = '%20'.join(args)
        else:
            return 'u need a query'
        url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=%s&key=%s&userip=%s' % (query, GOOGLE_API_KEY, MY_IP)
        request = urllib2.Request(url, None, {'Referer': 'http://quoth.notune.com'})
        try:
            response = urllib2.urlopen(request)
            results = json.load(response)['responseData']['results']
            result = '%s - %s' % (results[0]['titleNoFormatting'], results[0]['url'])
            return 'top result: %s' % str(result)
        except Exception as e:
            return 'ur shit am fuked: %s' % e
    
    @alias('gv', 'youtube', 'yt')
    @register
    def google_video(self, nick, host, channel, *args):
        """searches for videos"""
        if args:
            query = '%20'.join(args)
        else:
            return 'u need a query'
        url = 'https://ajax.googleapis.com/ajax/services/search/video?v=1.0&q=%s&key=%s&userip=%s' % (query, GOOGLE_API_KEY, MY_IP)
        request = urllib2.Request(url, None, {'Referer': 'http://quoth.notune.com'})
        try:
            response = urllib2.urlopen(request)
            results = json.load(response)['responseData']['results']
            title, url = results[0]['titleNoFormatting'], results[0]['url']
            if 'youtube' in url:
                url = re.search(YOUTUBE_PATTERN, url).group()
                url = url.replace('%3F', '?').replace('%3D', '=')
            return 'top result: %s' % str(' - '.join((title, url)))
        except Exception as e:
            return 'ur shit am fuked: %s' % e
    
