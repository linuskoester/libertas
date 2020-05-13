from django.urls import path

from . import views

urlpatterns = [
    path('<str:number>/<str:view_type>', views.viewer, name='viewer'),
    path('file/<str:identifier>/<str:view_type>', views.protected_file)
]
