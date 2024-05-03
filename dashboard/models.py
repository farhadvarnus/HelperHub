from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='ایمیل')

    is_author = models.BooleanField(
        default=False, verbose_name='وضعیت نویسندگی')
    spacial_user = models.DateTimeField(
        default=timezone.now, verbose_name='کاربر ویژه')

    def is_spacial_user(self):
        if self.spacial_user > timezone.now():
            return True
        else:
            return False

    is_spacial_user.boolean = True
    is_spacial_user.short_description = 'وضعیت کاربر ویژه'
