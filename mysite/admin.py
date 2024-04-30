from django.contrib import admin
from mysite.models import Contact

# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    list_display = ("name", "email", "subject",
                    "created_date", "updated_date")
    search_fields = ["name", "email"]


admin.site.register(Contact, ContactAdmin)
