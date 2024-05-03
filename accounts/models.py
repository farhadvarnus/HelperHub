from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='ایمیل')

    is_author = models.BooleanField(
        default=False, verbose_name='وضعیت نویسندگی')
    spacial_user = models.DateTimeField(
        default=timezone.now, verbose_name='کاربر ویژه')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="custom_user_permissions",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    def is_spacial_user(self):
        if self.spacial_user > timezone.now():
            return True
        else:
            return False

    is_spacial_user.boolean = True
    is_spacial_user.short_description = 'وضعیت کاربر ویژه'
