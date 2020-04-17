from django.urls import path
from . import views

urlpatterns = [
    path('', views.startseite, name='index'),  # Startseite
    path('podcast', views.podcast, name='podcast'),  # Podcast
    path('team', views.team, name='team'),  # Podcast
    path('faq', views.faq, name='faq'),  # Podcast
    path('redeem', views.redeem, name='redeem'),  # Code einlösen
]
