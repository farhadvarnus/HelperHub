from .views import *
from django.urls import path


app_name = 'blog'

urlpatterns = [
    path('', home_blog, name='index'),
    path('single/', single_blog, name='single'),


]
