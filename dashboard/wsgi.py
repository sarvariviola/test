"""
WSGI konfigurációs fájl a dashboard projekthez.
A WSGI callable-t elérhetővé teszi 'application' néven.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

application = get_wsgi_application()
