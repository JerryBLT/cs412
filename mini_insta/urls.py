# blog/urls.py
# author: Jerry Teixeira (jerrybt@bu.edu), 02/28/26
# discription: urls pathway for the apps
from django.urls import path
from .views import PostDetailView, ProfileDetailView, ProfileListView, CreatePostView, UpdateProfileView, DeletePostView, UpdatePostView

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="show_post"),
    path("post/<int:pk>/create_post/", CreatePostView.as_view(), name="create_post"),
    path("post/<int:pk>/delete/", DeletePostView.as_view(), name="delete_post"),
    path("profile/<int:pk>/update", UpdateProfileView.as_view(), name="update_profile"),
    path("profile/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),
    path("post/<int:pk>/update", UpdatePostView.as_view(), name="update_post"),

]
