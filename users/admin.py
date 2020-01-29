from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Django admin panel, fieldsets, plus custom panel

# Displayed on the user admin panel
# Decorator = this wants to use models.User onto CustomUserAdmin
@admin.register(models.User)  # = admin.site.register(models.User, CustomUserAdmin)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
    )
    list_filter = UserAdmin.list_filter + ("superhost",)
