# blog/urls.py
from django.urls import path
from .views import ProfileDetailView, ProfileListView

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="show_profile"),
    
]