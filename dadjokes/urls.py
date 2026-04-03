from django.urls import path
from . import views

urlpatterns = [
    path('', views.RandomJokeAndPictureView.as_view(), name='dadjokes_home'),
    path('random/', views.RandomJokeAndPictureView.as_view(), name='dadjokes_random'),
    path('jokes/', views.JokeListView.as_view(), name='dadjokes_jokes'),
    path('joke/<int:pk>/', views.JokeDetailView.as_view(), name='dadjokes_joke_detail'),
    path('pictures/', views.PictureListView.as_view(), name='dadjokes_pictures'),
    path('picture/<int:pk>/', views.PictureDetailView.as_view(), name='dadjokes_picture_detail'),

    # REST API
    path('api/', views.RandomJokeAPIView.as_view(), name='dadjokes_api_random'),
    path('api/random/', views.RandomJokeAPIView.as_view(), name='dadjokes_api_random_named'),
    path('api/jokes/', views.JokeListAPIView.as_view(), name='dadjokes_api_jokes'),
    path('api/joke/<int:pk>/', views.JokeDetailAPIView.as_view(), name='dadjokes_api_joke_detail'),
    path('api/pictures/', views.PictureListAPIView.as_view(), name='dadjokes_api_pictures'),
    path('api/picture/<int:pk>/', views.PictureDetailAPIView.as_view(), name='dadjokes_api_picture_detail'),
    path('api/random_picture/', views.RandomPictureAPIView.as_view(), name='dadjokes_api_random_picture'),
]
