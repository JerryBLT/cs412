# File: urls.py
# Author: Jerry Teixeira (jerrybt@bu.edu),01/25/2026
# Description: URL configuration for the quotes app.

from django.urls import path
from . import views

urlpatterns = [
    path("", views.quote, name="main"),          # "/"
    path("quote/", views.quote, name="quote"),   # "/quote" (same view as "/" )
    path("show_all/", views.show_all, name="show_all"),
    path("about/", views.about, name="about"),
]
