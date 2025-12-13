"""
URL konfigurációs fájl a dashboard projekthez.
Az urlpatterns lista tartalmazza az URL-ek és view-k közötti kapcsolatokat.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]
