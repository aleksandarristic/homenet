from django.contrib import admin

from dashboard.models import MenuURL, UrlGroup


@admin.register(MenuURL)
class MenuURLAdmin(admin.ModelAdmin):
    list_display = ('text', 'url', 'new_window', 'active', 'post_request', 'order', 'url_group', 'created', 'updated')
    list_filter = ('url_group', 'active', 'new_window', 'post_request')


@admin.register(UrlGroup)
class UrlGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'active')
    list_filter = ('active',)
