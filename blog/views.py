from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
import random
from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse 

# Create your views here.
class ShowAllView(ListView):
    '''defione a view class to show all blog Articles'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

class ArticleView(DetailView):
    '''Display a single article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

class RandomArticleView(DetailView):
    '''Display a single article display at random'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    #method
    def get_object(self):
        '''return one instance of the article object selected at random'''
        all_articles = Article.objects.all()
        article =  random.choice(all_articles)
        return article
    
# define a subclass of CreateView to handle the creation of Article onject
class CreateArticleView(CreateView):
    '''view to handle creation of a new article
    (1) display the HTML form to the user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

class CreateCommentView(CreateView):
    '''view to handle the creation of a new comment on an article.'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        '''provide a URL to redirect a user after successfully submitting the form.'''
        
        # create and return a URL:
        # return reverse('show_all') # redirect to the show all page
        # retrive the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to geenrate the URL for this article
        return reverse('article', kwargs={'pk': pk})
    
    def get_context_data(self):
        '''Return the dictionary of context cariables for use in the template.'''

        # calling the superclass method 
        context = super().get_context_data()

        # find/add article to the context data.
        # retireve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['article'] = article
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the
        new object to the Django databse.
        we need to add the foreign key (of the Article) to the Comment
        object before saving it to the databse.'''

        print(form.cleaned_data)
        # get the article_pk from the URL parameters
        pk = self.kwargs['pk']
        article = Article.objects.get(pk = pk)
        # attach this article to the comment
        form.instance.article = article # set the FK

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
