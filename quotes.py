import os, datetime
from chii import command

os.environ['DJANGO_SETTINGS_MODULE'] = 'quoth.settings'
from quoth.quotes.models import Quote

@command('q+')
def add_quote(self, channel, nick, host, *args):
    """adds quote to database"""
    q = Quote(nick=nick, host=host, channel=channel, added=datetime.datetime.now(), quote=' '.join(args))
    q.save()
    return 'added quote %d' % q.id

@command('q-')
def del_quote(self, channel, nick, host, *args):
    """deletes quote from database"""
    try:
        id = int(args[0])
        q = Quote.objects.get(id=id)
    except:
        return 'eh? what quote?'

    if q.host == host:
        q.delete()
        return 'deleted %d' % id
    else:
        return 'not your quote bub'

@command('q')
def quote(self, channel, nick, host, *args):
    """gets quotes from database random, by id, or search"""
    def rand():
        q = Quote.objects.order_by('?')
        if q:
            return str(q[0].quote)
        else:
            return 'quote not found'

    def get_id(q_id):
        q = Quote.objects.get_or_none(id=q_id)
        if q:
            return str(q.quote)
        else:
            return 'quote not found'

    def search(query):
        q = Quote.objects.filter(quote__icontains=query).order_by('?')
        if q:
            return str(q[0].quote)
        else:
            return 'quote not found'

    if args:
        try:
            return get_id(int(args[0]))
        except:
            return search(' '.join(args))
    else:
        return rand()
