# File: mini_insta/views.py
# Author: Jerry Teixeira jerrybt@bu.edu, 02/12/2026
# Discrition: View to display all user profiles in the mini_insta app.

from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Profile, Photo
from .forms import CreatePostForm
from django.urls import reverse

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

class CreatePostView(CreateView):
    '''view to display a create post in the mini_insta app'''
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    # Add profile into template context
    def get_context_data(self, **kwargs):
        '''Add the Profile (from URL pk) to context so the template can use it.'''
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['profile'] = Profile.objects.get(pk=pk)
        return context

    # Attach FK profile + create Photo
    def form_valid(self, form):
        '''This method handles the form submission and saves the
        new object to the Django databse.'''
        print(form.cleaned_data)

        # get the article_pk from the URL parameters
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.profile = profile # set the FK

        # Save the Post first so we can safely attach related Photo objects
        response = super().form_valid(form)

        photo_url = self.request.POST.get('photo_url', '').strip()
        if photo_url:
            Photo.objects.create(post=self.object, image_url=photo_url)

        return response

    # where to go after successful creation
    def get_success_url(self):
        return reverse('show_post', kwargs={'pk': self.object.pk})
    
