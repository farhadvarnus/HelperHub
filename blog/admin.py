from django.contrib import admin

from blog.models import Post, Category
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = "created_date"
    list_display = ("title", "author", "status", "counted_view",
                    "created_date", "updated_date")
    list_filter = ("status", "author")
    search_fields = ["title", "content"]
    summernote_fields = ['content']


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
