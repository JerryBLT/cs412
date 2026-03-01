# file: mini_insta/models.py
# author: Jerry Teixeira (jerrybt@bu.edu), 02/28/26
# discription: Class based views for Mini Instagram pages, inherits from django generic views
from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    '''A user profile model that extends the built-in User model.'''

    # model the data attributes of an individual user profile.
    username = models.TextField(blank = True)
    display_name = models.TextField(blank = True)
    bio_text = models.TextField(blank = True)
    join_date = models.DateTimeField(auto_now = True)
    profile_image_url = models.URLField(blank = True) # url as a string

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.display_name} ({self.username})"
    
    def get_all_posts(self):
        '''Return a list of all posts associated with this profile.'''
        post = Post.objects.filter(profile = self).order_by('timestamp')
        return post
    
    def get_absolute_url(self):
        '''Return the absolute URL for this profile detail page.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_followers(self):
        '''Return a list of Profile instances that follow this profile.'''
        follow_instances = Follow.objects.filter(profile=self)
        # iterate through follow_instances and get the follower_profile attribute
        followers = [follow.follower_profile for follow in follow_instances]
        return followers
    
    def get_num_followers(self):
        '''Return the number of followers this profile has.'''
        return Follow.objects.filter(profile=self).count()
    
    def get_num_following(self):
        '''Return the number of profiles this profile is following.'''
        return Follow.objects.filter(follower_profile=self).count()
    
    def get_following(self):
        '''Return a list of Profile instances that this profile is following.'''
        follow_instances = Follow.objects.filter(follower_profile=self)
        # iterate through follow_instances and get the profile attribute
        following = [following.profile for following in follow_instances] 
        return following

 
    
class Post(models.Model):
    '''A post model that represents a user's post on the platform.'''

    # model the data attributes of an individual post.
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now = True)
    caption = models.TextField(blank = True)

    def __str__(self):
        '''Return a string representation of this post instance.'''
        return f"{self.profile.username} posted on {self.timestamp} with caption: {self.caption}"
    
    def get_all_photos(self):
        '''Return a list of all photos associated with this post.'''
        photo = Photo.objects.filter(post = self).order_by('timestamp')
        return photo

    def get_all_comments(self):
        '''Return all comments made on this post ordered by newest first.'''
        return Comment.objects.filter(post=self).order_by('-timestamp')

    def get_likes(self):
        '''Return all likes associated with this post.'''
        return Like.objects.filter(post=self)
    
class Photo(models.Model):
    '''A photo model that represents a photo associated with a post.'''

    # model the data attributes of an individual photo.
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank = True) # url as a string
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now = True)

    def get_image_url(self):
        """Return the image URL if exists, otherwise return the image file URL.
        """
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return ''

    def __str__(self):
        '''Return a string representation of this photo instance.'''
        return f'image posted on {self.timestamp} by {self.post.profile.username}, image: {self.image_url if self.image_url else self.image_file}'

class Follow(models.Model):
    '''Encapsulates one profile following another'''

    # Profile being followed
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile")
    # Profile doing the following
    follower_profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this follow instance.'''
        return f'{self.follower_profile.username} followed {self.profile.username} on {self.timestamp}'


class Comment (models.Model):
    '''Represent a comment made by a profile on a post.'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this comment.'''
        return f'{self.profile.username} commented on {self.post.id} at {self.timestamp}: {self.text}'

class Like(models.Model):
    '''Represent a like made by a profile on a post.'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this like.'''
        return f'{self.profile.username} liked {self.post} at {self.timestamp}'
    
