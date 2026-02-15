from django.db import models

# Create your models here.

class Profile(models.Model):
    '''A user profile model that extends the built-in User model.'''

    # model the data attributes of an individual user profile.
    username = models.TextField(blank = True)
    display_name = models.TextField(blank = True)
    bio_text = models.TextField(blank = True)
    join_date = models.DateTimeField(auto_now = True)
    profile_image_url = models.URLField(blank = True)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.display_name} ({self.username})"
    
    def get_all_posts(self):
        '''Return a list of all posts associated with this profile.'''
        post = Post.objects.filter(profile = self).order_by('timestamp')
        return post
    
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
    
class Photo(models.Model):
    '''A photo model that represents a photo associated with a post.'''

    # model the data attributes of an individual photo.
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank = True)
    timestamp = models.DateTimeField(auto_now = True)

    def __str__(self):
        '''Return a string representation of this photo instance.'''
        return f"image posted on {self.timestamp} for post by {self.post.profile.username}, image: {self.image_url}"
