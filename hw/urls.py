# file hw/urls.py

from django.urls import path
from django.conf import settings
from . import views

# url patterns for hw app
urlpatterns = [
    # path('', views.home, name='hw_home'),
    path('', views.home_page, name='hw_home'),
    path('about/', views.about_page, name='hw_about'),
]

