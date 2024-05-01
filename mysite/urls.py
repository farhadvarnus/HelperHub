from .views import *
from django.urls import path


app_name = 'mysite'

urlpatterns = [
    path('', index_view, name='index'),
    path("contact", contact_view, name='contact'),


]
