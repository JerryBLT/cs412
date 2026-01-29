# File: quotes/views.py
# Author: Jerry Teixeira (jerrybt@bu.edu), 01/29/2026
# Description: Views for the quotes app that serves random quotes and images of Christiano Ronaldo.

from django.shortcuts import render
import random
# Create your views here.

# list[str]: list of quotes from Christiano Ronaldo.
quotes = [
    "I am not a perfectionist, but I like to feel that things are done well. More important than that, I feel an endless need to learn, to improve, to evolve.",
    "We cannot live being obsessed with what other people think of us. We have to learn to like ourselves as we are, accept our flaws and understand that we will not please everyone",
    "Dreams are not what you see in your sleep, dreams are things which do not let you sleep. I always want to do more, achieve more, and keep pushing the limits",
]

# list[str]: list of images urls from Christiano Ronaldo.
images = [
    "https://media.cnn.com/api/v1/images/stellar/prod/gettyimages-2234200789.jpg?c=original&q=w_860,c_fill",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Shahter-Reak_M_2015_%2818%29.jpg/250px-Shahter-Reak_M_2015_%2818%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Cristiano_Ronaldo_20120609.jpg/250px-Cristiano_Ronaldo_20120609.jpg",
]


def quote(request):
    '''Respond to the URL '' and '/quote' through displaying a random quote and image.'''
    
    # dict[str, str]: context data passed to the template, including a random quote and a random image.
    context ={
        "quote": random.choice(quotes), #return a random quote.
        "image": random.choice(images), #return a random image.
    } 

    # String, the path to the template to be rendered.
    template_name='quotes/quote.html'
    
    return render(request, template_name, context)

def show_all(request):
    '''Respond to the URL '/show_all' by displaying all quotes and images.'''
    
    # dict[str, list[str]]: context data passed to the template, including all quotes and images.
    context ={
        "quotes": quotes,
        "images": images,
    }
    
    # String, the path to the template to be rendered.
    template_name='quotes/show_all.html'

    return render(request, template_name, context)


def about(request):
    '''Respond to the URL '/about' with information about the site and Christiano Ronaldo.'''

    # String, the path to the template to be rendered.
    template_name = 'quotes/about.html'

    return render(request, template_name)