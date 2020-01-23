from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='libertas/login.html')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/?info=logout')),
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^account_activation_sent/$', views.account_activation_sent,
            name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),
]
