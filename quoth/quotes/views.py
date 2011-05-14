from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from coffin.shortcuts import render_to_response

from quoth.quotes.models import Quote

import _mysql
def get_db():
    return _mysql.connect(host="localhost",user="quoteengine", passwd="gibmequotes",db="quotes")

def list_raw(request):
    db = get_db()
    db.query('SELECT id, host, quote, timestamp FROM quotes ORDER BY id DESC LIMIT 25')
    r = db.use_result()
    quotes = [{"id": x[0], "nick": x[1], "quote": x[2], "timestamp": x[3]} for x in r.fetch_row(maxrows=0)]
    db.close()
    return HttpResponse(str(quotes), mimetype="text/plain")

def list_orm(request):
    quotes = [{"id": x.id, "nick": x.nick, "quote": x.quote, "timestamp": x.timestamp} for x in Quote.objects.order_by('-id')[:25]]
    return HttpResponse(str(quotes), mimetype="text/plain")

def index(request):
    queryset = Quote.objects.all().order_by('-id')
    return render_to_response('quotes/index.html', {'request': request, 'queryset': queryset})

def nick(request, nick):
    by_nick = Quote.objects.filter(nick__icontains=nick).order_by('-id')[:5]
    about_nick = Quote.objects.filter(quote__icontains=nick).order_by('-id')[:5]
    return render_to_response('quotes/nick.html', {'by_nick': by_nick, 'about_nick': about_nick, 'nick': nick})

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q', None)
    elif request.method == 'POST':
        query = request.POST.get('q', None)
    if query is not None:
        queryset = Quote.objects.filter(quote__icontains=query).order_by('-id')
        return render_to_response('quotes/search.html', {'request': request, 'queryset': queryset, 'query': query})
    else:
        raise Http404

def index_raw(request, page=None):
    db = _mysql.connect(host="localhost",user="quoteengine", passwd="gibmequotes",db="quotes")
    db.query('SELECT id, host, quote, timestamp FROM quotes ORDER BY id DESC LIMIT 25')
    r = db.use_result()
    quotes = [{"id": x[0], "nick": x[1], "quote": x[2], "timestamp": x[3]} for x in r.fetch_row(maxrows=0)]
    db.query('SELECT COUNT(quote) FROM quotes')
    r = db.use_result()
    count = int(r.fetch_row()[0][0])
    db.close()
    try:
        page = int(page)
    except:
        page = 1

    if page is 1 and (count > 25):
        paging = {'page': page, 'next': 2, 'prev': None}
    elif count > (page * 25):
        paging = {'page': page, 'next': page+1, 'prev': page-1}
    elif count < (page * 25):
        paging = {'page': page, 'next': None, 'prev': page-1}
    else:
        paging = None

    return render_to_response('quotes/index_raw.html', {'paging': paging, 'quotes': quotes})

def quote_raw(request, quote_id):
    try:
        pk = str(int(quote_id))
    except:
        raise Http404
    db.query('SELECT * FROM quotes WHERE id = %s' % pk)
    r = db.use_result()
    q = r.fetch_row()[0]
    return HttpResponse(q[0], mimetype="text/plain")

def quote_orm(request, quote_id):
    q = get_object_or_404(Quote, pk=quote_id)
    return HttpResponse(q.id, mimetype="text/plain")
    
def quote(request, quote_id):
    q = get_object_or_404(Quote, pk=quote_id)
    return render_to_response('quotes/quote.html', {'quote': q})

def vote(request, quote_id):
    q = get_object_or_404(Quote, pk=quote_id)
    try:
        selected_choice = q.choice_set.get(pk=request.POST['vote'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the Quote voting form.
        return render_to_response('quotes/quote.html', {
            'quote': q,
            'error_message': "You didn't select a quote.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('quoth.quotes.views.quote', args=(q.id,)))
