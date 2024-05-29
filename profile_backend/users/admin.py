from django.contrib import admin

from .models import ProfileUser, Code


@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'block_time'
    )
    list_filter = ('email',)
    search_fields = ('email',)
    list_display_links = ('email',)


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'code',
        'created_at'
    )
    list_display_links = ('user',)
