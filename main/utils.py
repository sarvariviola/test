from django.urls import path
# Itt a hiba: 'index' helyett 'dashboard_view'-t kell importálni
from django.urls import path
# A hiba itt volt: 'index' helyett most már 'dashboard_view' a neve
from .views import dashboard_view 

urlpatterns = [
    # új nézet hozzáadása
    path('', dashboard_view, name='dashboard'),
]