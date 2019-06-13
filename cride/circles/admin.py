"""Circles admmin"""
# Django
from django.contrib import admin

# Model
from cride.circles.models import Circle, Invitation, Membership


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Circle admin"""

    list_display = (
        'slug_name',
        'name',
        'is_public',
        'verified',
        'is_limited',
        'members_limit'
    )
    search_fields = ('slug_name', 'name')
    list_filter = (
        'is_public',
        'verified',
        'is_limited',
    )
admin.site.register(Membership)
admin.site.register(Invitation)
