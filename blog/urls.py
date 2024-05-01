from .views import *
from django.urls import path


app_name = 'blog'

urlpatterns = [
    path('', home_blog, name='index'),
    path("<int:pid>", single_blog, name='single'),
    path("category/<str:cat_name>", home_blog, name='category'),
    path("author/<str:author_username>", home_blog, name='author'),
    path("search/", search_blog, name='search'),
    path("tags/<str:tag_name>", home_blog, name='tag'),


]
