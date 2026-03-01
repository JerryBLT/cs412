# file: mini_insta/admin.py
# author: Jerry Teixeira (jerrybt@bu.edu), 02/28/26
# discription: register all models
from django.contrib import admin

# Register your models here.
from .models import Post, Profile, Photo, Follow, Comment, Like
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)
