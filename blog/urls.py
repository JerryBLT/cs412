# blog/urls.py
from django.urls import path
from .views import * #showAllView, ArticleView, RandomArticleView

urlpatterns = [
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all/', ShowAllView.as_view(), name="show_all"),
    path('article/<int:pk>/', ArticleView.as_view(), name="article"),
    path('article/create/', CreateArticleView.as_view(), name="create_article"), #new
    path('article/<int:pk>/create_comment/', CreateCommentView.as_view(), name="create_comment"), #new
]