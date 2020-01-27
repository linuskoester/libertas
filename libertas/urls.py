from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Authentication
    path('signin/', views.signin, name='signin'),
    path('signout/', auth_views.LogoutView.as_view(next_page='/?info=signout'), name='signout'),
    path('signup/', views.signup, name='signup'),
    path('signup/sent', views.signup_sent, name='signup_sent'),
    re_path(r'^signup/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.signup_activate, name='signup_activate'),
    path('reset/', views.reset, name='reset'),
    path('reset/sent', views.reset_sent, name='reset_sent'),
    re_path(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.reset_confirm, name='reset_confirm'),
    path('reset/success', views.reset_success, name='reset_success')
]
