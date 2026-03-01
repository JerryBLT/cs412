# file: mini_insta/forms.py
# Author: Jerry Teixeira jerrybt@bu.edu, 02/14/2026
# Disciption: define the form that we will use for create/delete/update operations
from django import forms
from .models import *

class CreatePostForm(forms.ModelForm): 
    '''Create a form to submit a new post caption'''
    class Meta:
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''Update a profile form'''
    class Meta:
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image_url']
