from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.startseite, name='index'),  # Startseite
    path('podcast', views.podcast, name='podcast'),  # Podcast
    path('team', views.team, name='team'),  # Podcast
    path('faq', views.faq, name='faq'),  # Podcast
    path('redeem', views.redeem, name='redeem'),  # Code einlösen
    path('datenschutz', views.datenschutz, name='datenschutz'),  # Datenschutz
    path('impressum', views.impressum, name='impressum'),  # Impressum
    path('agb', views.agb, name='agb'),  # AGB
    path('corona', RedirectView.as_view(url='buy')),  # Corona-Infos
    path('buy', views.buy, name='corona'),  # Kaufen
    path('buy', views.buy, name='buy'),  # Kaufen
]
