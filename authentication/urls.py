from django.urls import path, re_path
from . import views

urlpatterns = [
    # An-/Abmeldung
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    # Registrierung
    path('signup/', views.signup, name='signup'),
    re_path(r'^signup/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.signup_activate, name='signup_activate'),
    # Passwort zurücksetzen
    path('reset/', views.reset, name='reset'),
    re_path(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.reset_confirm, name='reset_confirm'),
    # Account-Verwaltung
    path('account/', views.account_info, name='account'),
    path('account/password', views.account_password, name='account_password'),
    path('account/delete', views.account_delete, name='account_delete'),
]
