"""
ASGI konfigurációs fájl a dashboard projekthez.
Az ASGI callable-t elérhetővé teszi 'application' néven.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

application = get_asgi_application()
