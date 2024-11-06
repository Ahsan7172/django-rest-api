from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin 
# Register your models here.
class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "name","image","is_admin","is_active","created_at","updated_at"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User crenditials",{"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name","image"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name","image", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)