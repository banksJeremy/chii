from django.utils.safestring import mark_safe
from django.template import RequestContext
from django.shortcuts import render
from jinja2 import Markup

from paging.helpers import paginate as paginate_func

def paginate(request, queryset_or_list, per_page=25):
    context_instance = RequestContext(request)
    context = paginate_func(request, queryset_or_list, per_page)
    paging = Markup(render(request, 'paging/pager.html', context, context_instance))
    return dict(objects=context['paginator'].get('objects', []), paging=paging)
