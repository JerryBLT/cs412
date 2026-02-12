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