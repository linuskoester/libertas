from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='libertas/login.html')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/?info=logout'))
]