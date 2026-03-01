# File: mini_insta/views.py
# Author: Jerry Teixeira jerrybt@bu.edu, 02/12/2026
# Discrition: View to display all user profiles in the mini_insta app.

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Profile, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
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

        # photo_url = self.request.POST.get('photo_url', '').strip()
        # if photo_url:
        #     Photo.objects.create(post=self.object, image_url=photo_url)
        
        files = self.request.FILES.getlist('files')
        for file in files:
            Photo.objects.create(post=self.object, image_file=file)

        return response

    # where to go after successful creation
    def get_success_url(self):
        return reverse('show_post', kwargs={'pk': self.object.pk})
    

class UpdateProfileView(UpdateView):
    '''View to update the user profile'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'


class DeletePostView(DeleteView):
    '''View to delete a post in the mini_insta app.'''
    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_context_data(self, **kwargs):
        '''Add the Post and its Profile to the template context.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context

    def get_success_url(self):
        """Return to the profile page after deleting a post."""
        return self.object.profile.get_absolute_url()
    
class UpdatePostView(UpdateView):
    """Update a Post, redirect to that post's detail page after save."""

    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"
    context_object_name = 'post'

    def get_success_url(self):
        """Return to the profile page after deleting a post."""
        return self.object.profile.get_absolute_url()


class ShowFollowersDetailView(DetailView):
    '''Display the followers for a Profile.'''

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
    '''Display the profiles this Profile is following.'''

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"
