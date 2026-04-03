import random

from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer
from rest_framework import generics
from rest_framework.response import Response


# Web views

class RandomJokeAndPictureView(ListView):
    '''Display a random joke and picture on the home page'''
    
    model = Joke
    template_name = "dadjokes/random.html"
    context_object_name = "joke"
    
    def get_context_data(self, **kwargs):
        '''Override to add picture to context'''
        context = super().get_context_data(**kwargs)
        context['joke'] = Joke.objects.order_by('?').first()
        context['picture'] = Picture.objects.order_by('?').first()
        return context
    
    def get_queryset(self):
        '''Not used, but required by ListView'''
        return Joke.objects.none()


class JokeListView(ListView):
    '''Display all jokes'''
    
    model = Joke
    template_name = "dadjokes/jokes.html"
    context_object_name = "jokes"
    
    def get_queryset(self):
        '''Return all jokes ordered by creation date'''
        return Joke.objects.all().order_by('-created')


class JokeDetailView(DetailView):
    '''Display a single joke by primary key'''
    
    model = Joke
    template_name = "dadjokes/joke_detail.html"
    context_object_name = "joke"


class PictureListView(ListView):
    '''Display all pictures'''
    
    model = Picture
    template_name = "dadjokes/pictures.html"
    context_object_name = "pictures"
    
    def get_queryset(self):
        '''Return all pictures ordered by creation date'''
        return Picture.objects.all().order_by('-created')


class PictureDetailView(DetailView):
    '''Display a single picture by primary key'''
    
    model = Picture
    template_name = "dadjokes/picture_detail.html"
    context_object_name = "picture"


# API views

class RandomJokeAPIView(generics.GenericAPIView):
    '''API endpoint to return a random joke as JSON'''
        
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer
    
    def get(self, request):
        '''Handle GET requests to return a random joke.'''
        random_joke = Joke.get_random_joke()
        serializer = self.get_serializer(random_joke)
        return Response(serializer.data)


class JokeListAPIView(generics.ListCreateAPIView):
    '''API endpoint to list all jokes and create new jokes'''
    
    queryset = Joke.objects.all().order_by('-created')
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveAPIView):
    '''API endpoint to retrieve a single joke by primary key'''
    
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class RandomPictureAPIView(generics.GenericAPIView):
    '''API endpoint to return a random picture as JSON'''
    
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    
    def get(self, request):
        '''Handle GET requests to return a random picture.'''
        picture = Picture.objects.order_by('?').first()
        serializer = self.get_serializer(picture)
        return Response(serializer.data)


class PictureListAPIView(generics.ListAPIView):
    '''API endpoint to list all pictures'''
    
    queryset = Picture.objects.all().order_by('-created')
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveAPIView):
    '''API endpoint to retrieve a single picture by primary key'''
    
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

