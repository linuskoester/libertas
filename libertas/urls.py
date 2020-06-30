from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.startseite, name='index'),
    path('podcast', views.podcast, name='podcast'),
    path('team', views.team, name='team'),
    path('faq', views.faq, name='faq'),
    path('redeem', views.redeem, name='redeem'),
    path('datenschutz', views.datenschutz, name='datenschutz'),
    path('impressum', views.impressum, name='impressum'),
    path('agb', views.agb, name='agb'),
    path('corona', RedirectView.as_view(url='buy')),
    path('buy', views.buy, name='corona'),
    path('buy', views.buy, name='buy'),
    path('ausgaben', views.ausgaben, name='ausgaben'),
    path('news', views.news, name='news'),
    # path('error404', views.error404, name='error404'),
    # path('error500', views.error500, name='error500'),
]

handler404 = 'libertas.views.error404'
handler500 = 'libertas.views.error500'
