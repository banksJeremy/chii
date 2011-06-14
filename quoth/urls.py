from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from quoth.quotes.urls import urlpatterns

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)
