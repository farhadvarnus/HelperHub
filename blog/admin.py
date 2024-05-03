from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_summernote.admin import SummernoteModelAdmin

from blog.models import Post, Category
from accounts.models import User
# Register your models here.


# class PostAdmin(SummernoteModelAdmin):
#     date_hierarchy = "created_date"
#     list_display = ("title", "author", "status", "counted_view",
#                     "created_date", "updated_date",)
#     list_filter = ("status", "author")
#     search_fields = ["title", "content"]
#     summernote_fields = ('content',)


UserAdmin.fieldsets[2][1]['fields'] = (
    "is_active",
    "is_staff",
    "is_superuser",
    "is_author",
    "spacial_user",
    "groups",
    "user_permissions",
)
UserAdmin.list_display += ('is_author', 'is_spacial_user')


# admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)

admin.site.register(Category)
