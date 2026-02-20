# blog/urls.py
from django.urls import path
from .views import PostDetailView, ProfileDetailView, ProfileListView, CreatePostView

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="show_post"),
    path("post/<int:pk>/create_post/", CreatePostView.as_view(), name="create_post")
]