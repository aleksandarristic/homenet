from django.contrib import admin

from speedtest.models import SpeedTest, PingTest, DnsTest

admin.site.register(SpeedTest, list_display=('start_time', 'server', 'download', 'upload', 'latency', 'success',
                                             'duration', 'is_average'))
admin.site.register(PingTest, list_display=('start_time', 'server', 'ping', 'packet_loss', 'success', 'duration'))
admin.site.register(DnsTest, list_display=('start_time', 'server', 'ip', 'success', 'duration'))
