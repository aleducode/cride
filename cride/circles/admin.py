"""Circles admmin"""
#Django
from django.contrib import admin

#Model
from cride.circles.models import Circle

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Circle admin"""

    list_display=(
        'slug_name',
        'name',
        'is_public',
        'verified',
        'is_limited',
        'member_list'
    )
    search_fields=('slug_name','name')
    list_filter=(
        'is_public',
        'verified',
        'is_limited',
    )