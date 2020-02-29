from django.urls import path
from . import views

urlpatterns = [
    path('<str:pdf>/', views.viewer)
]
