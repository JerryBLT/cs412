# file: blog/forms.py
# define the form that we will use for create/delete/update operations
from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    '''A form to add an article to the databse.'''

    class Meta:
        '''Associate this form with an article form our databse'''
        model = Article
        # fields = ['author', 'title', 'text', 'image_url']
        fields = ['author', 'title', 'text', 'image_file']

class UpdateArticleForm(forms.ModelForm):
    '''A form to update the article databse.'''

    class Meta:
        '''Associate this form with an model in our database'''
        model = Article
        fields = ['title', 'text'] #fields to update


class CreateCommentForm(forms.ModelForm):
    '''A form to add a comment to the database.'''

    class Meta:
        '''Associate this form with a model form from our database'''
        model = Comment
        # fields = ['article', 'author', 'text']
        fields = ['author', 'text'] # we don't want the drop-down list
