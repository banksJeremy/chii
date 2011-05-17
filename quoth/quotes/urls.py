from django.conf.urls.defaults import *

urlpatterns = patterns('quoth.quotes.views',
    (r'^$', 'index'),
    (r'^search$', 'search'),
    (r'^nick/(\w+)/$', 'nick'),
    (r'^quote/(\d+)/$', 'quote'),
    (r'^list_raw/', 'list_raw'),
    (r'^list_orm/', 'list_orm'),
    (r'^index_raw/', 'index_raw'),
    (r'^index_raw/(\d+)/', 'index_raw'),
    (r'^quote_raw/(\d+)/$', 'quote_raw'),
    (r'^quote_orm/(\d+)/$', 'quote_orm'),
    (r'^(\d+)/vote/(\d{1})$', 'vote'),
)
