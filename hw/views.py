# file hw/views.py

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import time
import random
# Create your views here.
# def home(request):
#     '''View function for home page of hw app.'''

#     respose_text = f'''<html> <h1>Hello World from HW app!</h1>
#     <p>Current server time is: {time.ctime()}</p> </html>
#     '''

#     return HttpResponse(respose_text)

def home_page(request):
    '''View function for home page of hw app.'''

    template_name = 'hw/home.html'
    # a dic of context variables to pass to the template
    context = {
        'current_time': time.ctime(),
        "letter1": chr(random.randint(65, 90)),
        "letter2": chr(random.randint(65, 90)),
        "number": random.randint(1, 100)
    } 
    return render(request, template_name, context)

def about_page(request):
    '''View function for about page of hw app.'''

    template_name = 'hw/about.html'
    # a dic of context variables to pass to the template
    context = {
        'current_time': time.ctime(),
        "number": random.randint(1, 100)
    } 
    return render(request, template_name, context)



