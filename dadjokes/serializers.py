from rest_framework import serializers
from .models import Joke, Picture


class JokeSerializer(serializers.ModelSerializer):
    '''A serializer for the Joke model.
    Specify which model/fields to send in the API.'''
    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'created']


class PictureSerializer(serializers.ModelSerializer):
    '''A serializer for the Picture model.
    Specify which model/fields to send in the API.'''
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'created']
