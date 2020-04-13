from django.urls import path
from . import views

urlpatterns = [
    path('', views.startseite, name='index'),  # Startseite
    path('redeem', views.redeem, name='redeem'),  # Code einlösen
]
