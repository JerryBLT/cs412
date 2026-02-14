from django.db import models
from django.urls import reverse
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
    
    def get_absolute_url(self):
        '''Return the url to display one isntance of this object.'''
        return reverse('article', kwargs={'pk': self.pk})
    
    def get_all_comments(self):
        '''Return a QuerySet of comments about this article.'''
        # use the object manager to retrieve comments about this article
        comments = Comment.objects.filter(article = self)
        return comments

class Comment(models.Model):
    '''Encapsulates the idea of a comment on an article.'''

    # data attributes for the comment
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank = True)
    text = models.TextField(blank = True)
    published = models.DateTimeField(auto_now = True)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f"{self.text} by {self.author}"