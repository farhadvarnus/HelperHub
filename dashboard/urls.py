from django.urls import path
from .views import (
    Article_list,
    Article_Create,
    Article_Update,
    AuthorDelete,
    Profile,
    PasswordChange,
    PasswordChangeDoneView,

)

app_name = 'dashboard'
urlpatterns = [
    path('', Article_list.as_view(), name='home'),
    path('article/create', Article_Create.as_view(),
         name='article-create'),
    path('article/update/<int:pk>',
         Article_Update.as_view(), name='article-update'),
    path('article/delete/<int:pk>', AuthorDelete.as_view(),
         name='article-delete'),
    path('profile/', Profile.as_view(), name='profile'),

    path(
        "password_change/", PasswordChange.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
