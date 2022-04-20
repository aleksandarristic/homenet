from django.contrib import admin

from dashboard.models import MenuURL, UrlGroup


@admin.register(MenuURL)
class MenuURLAdmin(admin.ModelAdmin):
    list_display = ('text', 'url', 'new_window', 'active', 'order', 'url_group', 'created', 'updated')


@admin.register(UrlGroup)
class UrlGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'active')
