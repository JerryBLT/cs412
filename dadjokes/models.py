from django.db import models
from random import randint

# Create your models here.

class Joke(models.Model):
    '''Represents a joke for the DadJokes application'''
    text = models.TextField(blank = True)
    contributor = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)

    def get_random_joke():
        '''Obtain a random joke from querying all jokes and randomly indexing.'''
        num_jokes = Joke.objects.count()
        if num_jokes == 0:
            return None
        
        j_index = randint(0, num_jokes - 1)
        joke = Joke.objects.all()[j_index]
        return joke

    def __str__(self):
        return f"{self.text[:50]}... ({self.contributor})"


class Picture(models.Model):
    '''Represents an image for the DadJokes application.'''

    image_url = models.URLField(blank = True)
    contributor = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)

    def get_image_url(self):
        """Return the image URL."""
        return self.image_url
    
    def get_random_picture_url():
        """Return a random image url."""
        num_pictures = Picture.objects.count()
        if num_pictures == 0:
            return ""
        
        p_index = randint(0, num_pictures - 1)
        picture = Picture.objects.all()[p_index]
        return picture.get_image_url()

    def __str__(self):
        return f"{self.image_url} ({self.contributor})"
