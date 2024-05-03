from . import views
from django.urls import path


app_name = 'blog'

urlpatterns = [
    path('', views.home_blog, name='index'),
    path("<int:pid>", views.single_blog, name='single'),
    path("category/<str:cat_name>", views.home_blog, name='category'),
    path("author/<str:author_username>", views.home_blog, name='author'),
    path("search/", views.search_blog, name='search'),
    path("tags/<str:tag_name>", views.home_blog, name='tag'),

    path('article/create', views.Article_Create.as_view(),
         name='article-create'),  # تعیین مسیر برای اضافه کردن مقاله
    path('article/update/<int:pk>',
         views.Article_Update.as_view(), name='article-update'),
    path('article/delete/<int:pk>',
         views.AuthorDelete.as_view(), name='article-delete'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('article/<slug:slug>', views.Detail_list.as_view(), name='detail_article'),



]
