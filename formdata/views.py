from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def show_form(request):
    """show the form to the user."""
    template_name = 'formdata/form.html'
    return render(request, template_name)


def submit(request):
    """Process the form submisssion and generate a result."""
    
    print(request)

    template_name = 'formdata/confirmation.html'

    # check if post data was sent with HTTP POST message
    if request.POST:
        # extract the field into variables
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        #create context dictionary to send to template
        context = {
            'name': name,
            'color': favorite_color,
        }

    # delegate the resposnse to the template, provide context variable
    return render(request, template_name = template_name, context=context)
