from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random

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
    
   