from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Startseite
    path('redeem/<str:number>', views.redeem, name='redeem'),  # Token einlösen
]
