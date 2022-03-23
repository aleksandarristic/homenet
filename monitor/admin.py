from django.contrib import admin

from monitor.models import Device, Scan


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'first_seen', 'last_seen', 'mac_address', 'last_ip', 'scan_count')
    search_fields = ('name', 'type', 'manufacturer', 'last_ip', 'mac_address')

    def scan_count(self, obj):
        return obj.scan_set.count()


@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ('time', 'type', 'command')
