from django.contrib import admin

from dashboard.models import MenuURL


@admin.register(MenuURL)
class MenuURLAdmin(admin.ModelAdmin):
    list_display = ('text', 'url', 'active', 'order', 'created', 'updated')
