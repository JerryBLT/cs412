# File: mini_insta/views.py
# Author: Jerry Teixeira jerrybt@bu.edu, 02/12/2026
# Discrition: View to display all user profiles in the mini_insta app.

from django.views.generic import ListView, DetailView
from .models import Post, Profile

class ProfileListView(ListView):
    '''View to display all user profiles in the mini_insta app.'''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''View to display a single user profile in the mini_insta app.'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    '''View to display a single post in the mini_insta app.'''
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"