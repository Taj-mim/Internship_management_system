from django.contrib import admin
from accounts.models import Apply

from .models import (
    Job,
    Bookmark,
    UserProfile
)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'organization',
        'location',
        'job_type',
        'deadline'
    )

    search_fields = (
        'title',
        'organization',
        'location'
    )


@admin.register(Apply)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'job',
        'email',
        'applied_date'
    )

    search_fields = (
        'full_name',
        'email'
    )


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'job',
        'created_at'
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'role'
    )

    list_filter = (
        'role',
    )