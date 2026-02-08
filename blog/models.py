from django.db import models

# Create your models here.

class Article(models.Model):
    '''Encapsulates the data of a blog article by author.'''

    #define the data atrribute of the article object
    title = models.TextField(blank = True)
    author = models.TextField(blank = True)
    text = models.TextField(blank = True)
    published = models.DateTimeField(auto_now = True)
    image_url = models.URLField(blank = True)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.title} by {self.author}"
    

