from django.test import TestCase
from django.contrib import admin
from django.urls import path, include
# Create your tests here.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('formdata/', include("formdata.urls")),
]