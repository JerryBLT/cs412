# File: mini_insta/views.py
# Author: Jerry Teixeira jerrybt@bu.edu, 02/12/2026
# Discrition: View to display all user profiles in the mini_insta app.

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from .models import Post, Profile, Photo, Follow, Like, Comment
from .forms import CreatePostForm, CreateProfileForm, UpdateProfileForm, UpdatePostForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


class ProfileAuthMixin(LoginRequiredMixin):
    '''Require authentication and provide the currently logged-in Profile.'''
    
    def get_login_url(self):
        '''Obtain the url that displays the login form.'''
        return reverse('login')

    def get_logged_in_profile(self):
        '''Return the Profile for the currently authenticated user.'''
        profile = Profile.objects.filter(user=self.request.user).first()
        if profile is None:
            raise PermissionDenied("No profile is linked to this user.")
        return profile


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

    def get_context_data(self, **kwargs):
        '''Add logged-in profile context for follow button visibility.'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        
        logged_in_profile = None
        is_following_profile = False
        if self.request.user.is_authenticated:
            logged_in_profile = Profile.objects.filter(user=self.request.user).first()
            if logged_in_profile is not None and logged_in_profile.pk != profile.pk:
                is_following_profile = logged_in_profile.is_following(profile)

        context['logged_in_profile'] = logged_in_profile
        context['is_following_profile'] = is_following_profile
        return context

class PostDetailView(DetailView):
    '''View to display a single post in the mini_insta app.'''
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        '''Add logged-in profile and like status for like/unlike action buttons.'''
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        logged_in_profile = None
        has_liked = False
        if self.request.user.is_authenticated:
            logged_in_profile = Profile.objects.filter(user=self.request.user).first()
            if logged_in_profile is not None:
                has_liked = post.is_liked_by(logged_in_profile)

        context['logged_in_profile'] = logged_in_profile
        context['has_liked'] = has_liked
        return context

class CreatePostView(ProfileAuthMixin, CreateView):
    '''view to display a create post in the mini_insta app'''
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    # Add profile into template context
    def get_context_data(self, **kwargs):
        '''Add the logged-in Profile to context so the template can use it.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_logged_in_profile()
        return context

    # Attach FK profile + create Photo
    def form_valid(self, form):
        '''This method handles the form submission and saves the
        new object to the Django databse.'''
        print(form.cleaned_data)

        # attach this profile to the post
        profile = self.get_logged_in_profile()
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
    

class UpdateProfileView(ProfileAuthMixin, UpdateView):
    '''View to update the user profile'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self, queryset=None):
        """Return the logged-in user profile."""
        return self.get_logged_in_profile()


class DeletePostView(ProfileAuthMixin, DeleteView):
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
    
class UpdatePostView(ProfileAuthMixin, UpdateView):
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


class PostFeedListView(ProfileAuthMixin, ListView):
    '''List the post feed for a single Profile (posts from profiles they follow).'''

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Return the feed of Posts for the logged-in profile."""
        profile = self.get_logged_in_profile()
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        """Add the profile (feed owner) to context for the template."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_logged_in_profile()
        return context


class SearchView(ProfileAuthMixin, ListView):
    '''Search Profiles and Posts on behalf of a Profile.'''

    model = Post
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        '''If query is absent/blank in GET, show search form; otherwise run ListView.'''

        query = request.GET.get('query', '').strip()
        if not query:
            # When there is no search query, show the form page instead of results.
            profile = self.get_logged_in_profile()
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
        context['profile'] = self.get_logged_in_profile()

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

class MyProfileView(ProfileAuthMixin, DetailView):
    '''View to show the logged-in user profile.'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        '''Return the profile associated with request.user.'''
        return self.get_logged_in_profile()

class CreateProfileView(CreateView):
    '''Create both a Django User and linked Profile in one submission.'''
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        '''Pass a UserCreationForm to the template along with profile form context.'''
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context 

    def get_success_url(self):
        return reverse('my_profile')

    def form_valid(self, form):
        '''Create and log in the user before saving the profile with user FK.'''
        user_form = UserCreationForm(self.request.POST)

        if not user_form.is_valid():
            return self.form_invalid(form)

        user = user_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user
        return super().form_valid(form)

    def form_invalid(self, form):
        '''Re-render with both bound forms and validation errors.'''
        context = self.get_context_data(form=form, user_form=UserCreationForm(self.request.POST))
        return self.render_to_response(context)


class FollowProfileView(ProfileAuthMixin, View):
    '''Create a follow relationship from logged-in user to target profile.'''

    def dispatch(self, request, *args, **kwargs):
        user = self.get_logged_in_profile()
        view_profile = Profile.objects.get(pk=kwargs['pk'])

        if user == view_profile: 
            return redirect(user.get_absolute_url())
        
        Follow.objects.get_or_create(follower_profile=user, profile=view_profile)
        return redirect(view_profile.get_absolute_url())


class DeleteFollowProfileView(ProfileAuthMixin, View):
    '''Remove a follow relationship from logged-in user to target profile.'''

    def dispatch(self, request, *args, **kwargs):
        '''Remove the Follow unless it is the user's own profile, then redirect back.'''
        user = self.get_logged_in_profile()
        view_profile = Profile.objects.get(pk=kwargs['pk'])

        if user == view_profile: 
            return redirect(user.get_absolute_url())
        
        Follow.objects.filter(follower_profile=user, profile=view_profile).delete()
        return redirect(view_profile.get_absolute_url())


class LikePostView(ProfileAuthMixin, View):
    '''Create a like on a post from the logged-in profile.'''

    def dispatch(self, request, *args, **kwargs):
        user = self.get_logged_in_profile()
        post = Post.objects.get(pk=kwargs['pk'])

        if user == post.profile: 
            return redirect(user.get_absolute_url())
        
        Like.objects.get_or_create(post=post, profile=user)
        return redirect(post.get_absolute_url())


class DeleteLikePostView(ProfileAuthMixin, View):
    '''Delete a like on a post from the logged-in profile.'''

    def dispatch(self, request, *args, **kwargs):
        user = self.get_logged_in_profile()
        post = Post.objects.get(pk=kwargs['pk'])

        if user ==post.profile: 
            return redirect(user.get_absolute_url())
        
        Like.objects.filter(post=post, profile=user).delete()
        return redirect(post.get_absolute_url())


class CreateCommentView(ProfileAuthMixin, View):
    '''Create a comment on a post from the logged-in profile.'''

    def dispatch(self, request, *args, **kwargs):
        commenter = self.get_logged_in_profile()
        post = Post.objects.get(pk=kwargs['pk'])
        text = (request.POST.get('text') or '').strip()
        if text:
            Comment.objects.create(post=post, profile=commenter, text=text)
        return redirect('show_post', pk=post.pk)