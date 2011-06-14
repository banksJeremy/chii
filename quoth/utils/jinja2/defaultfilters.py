from django.conf import settings

def urlencode(value):
    from django.template.defaultfilters import urlencode
    return urlencode(value)

def linebreaks(value):
    from django.template.defaultfilters import linebreaks
    return linebreaks(value)

def intcomma(value):
    from django.contrib.humanize.templatetags.humanize import intcomma
    return intcomma(value)

def truncatechars(value, length=30):
    if len(value) > length:
        value = value[0:length-3] + '...'
    return value

try:
    from cmath import math
except ImportError:
    import math

def ceil(value):
    return math.ceil(value)

def floor(value):
    return math.floor(value)

def timesince(value):
    from django.template.defaultfilters import timesince
    value = (' '.join(timesince(value).split(' ')[0:2])).strip(',')
    if value == '0 minutes':
        return 'Just now'
    return value + ' ago'

import os, os.path
def mediaversion(value):
    """Returns the modified time (as a string) for the media"""
    try:
        fname = os.path.abspath(os.path.join(settings.STATIC_ROOT, value))
        if not fname.startswith(settings.PROJECT_ROOT):
            raise ValueError("Media must be located within STATIC_ROOT.")
        return unicode(int(os.stat(fname).st_mtime))
    except OSError:
        return 0

def mediaurl(value, arg=None):
    return "%s%s?%s" % (settings.STATIC_URL, value, mediaversion(value))


