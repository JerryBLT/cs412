# File: urls.py
# Author: Jerry Teixeira (jerrybt@bu.edu),01/31/2026
# Description: URL configuration for the restaurant app.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),         # "/restaurant/"
    path('order/', views.order, name='order'),       # "/restaurant/order/"
    path('confirmation/', views.confirmation, name='confirmation'), # "/restaurant/confirmation/"
]