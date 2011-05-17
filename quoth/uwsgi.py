# uwsgi.py for hotloading with nginx & uwsgi in a virtualenv
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'quoth.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
