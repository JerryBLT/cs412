# File: mini_insta/views.py
# Author: Jerry Teixeira jerrybt@bu.edu, 02/12/2026
# Discrition: View to display all user profiles in the mini_insta app.

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.shortcuts import render
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
    context_object_name = 'post'

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
        """Return to the post detail page after updating a post."""
        return reverse('show_post', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """Provide the post and its profile for the update form template."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context


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


class PostFeedListView(ListView):
    '''List the post feed for a single Profile (posts from profiles they follow).'''

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Return the feed of Posts for the profile identified by URL pk."""
        # Profile whose feed we are showing (pk from URL):
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        """Add the profile (feed owner) to context for the template."""
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context


class SearchView(ListView):
    '''Search Profiles and Posts on behalf of a Profile.'''

    model = Post
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        '''If query is absent/blank in GET, show search form; otherwise run ListView.'''

        query = request.GET.get('query', '').strip()
        if not query:
            # When there is no search query, show the form page instead of results.
            pk = kwargs.get('pk')
            profile = Profile.objects.get(pk=pk)
            return render(request, 'mini_insta/search.html', {'profile': profile})
        
        # Otherwise let ListView handle the request and show search_results.html.
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''Return Posts whose caption contains the query string.'''
        query = self.request.GET.get('query', '').strip()
        if not query:
            return Post.objects.none()
        return Post.objects.filter(caption__icontains=query).order_by('-timestamp')
    
    def get_context_data(self, **kwargs):
        '''Add profile, query, and matching profiles to context; posts from get_queryset.'''
        context = super().get_context_data(**kwargs)
        # Profile we are searching
        pk = self.kwargs['pk']
        context['profile'] = Profile.objects.get(pk=pk)

        # Search term for display and for filtering profiles
        query = self.request.GET.get('query', '').strip()
        context['query'] = query

        # Profiles matching query in username, display_name, or bio_text
        context['profiles'] = Profile.objects.filter(
            Q(username__icontains=query) |
            Q(display_name__icontains=query) |
            Q(bio_text__icontains=query)
        )
        return context
