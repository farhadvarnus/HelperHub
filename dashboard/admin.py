from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import User

UserAdmin.fieldsets [2][1]['fields'] = ( # افزودن قسمت به فیلد مورد نظر
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_author",
                    "spacial_user",
                    "groups",
                    "user_permissions",
)

UserAdmin.list_display += ('is_author' , 'is_spacial_user') # برای نمایش وضعیتشون در منو بار کاربرها

# Register your models here.
admin.site.register(User, UserAdmin)