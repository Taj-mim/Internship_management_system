from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    # =====================================================
    # USER LIST
    # =====================================================

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
    )

    # =====================================================
    # FILTERS
    # =====================================================

    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )

    # =====================================================
    # SEARCH
    # =====================================================

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    # =====================================================
    # EDIT USER
    # =====================================================

    fieldsets = UserAdmin.fieldsets + (
        (
            "Role Information",
            {
                "fields": (
                    "role",
                )
            },
        ),
    )

    # =====================================================
    # ADD USER
    # =====================================================

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Role Information",
            {
                "fields": (
                    "role",
                )
            },
        ),
    )