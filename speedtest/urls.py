from django.urls import path, register_converter

from common.url_converters import DateConverter
from speedtest import views

register_converter(DateConverter, 'date')
app_name = 'speedtest'

urlpatterns = [
    path('', views.index, name='index'),
    path('day/<date:day>/', views.index, name='day_detail'),
    path('speed/<int:entry_id>/', views.speedtest_detail, name='entry_detail'),
    path('speed/start/', views.speedtest_start, name='speedtest_start'),
    path('speed/stop/<int:entry_id>/', views.speedtest_stop, name='speedtest_stop'),
    path('speed/stop/all/', views.speedtest_stop, name='speedtest_stop_all'),
    path('ping/<int:entry_id>/', views.pingtest_detail, name='pingtest_detail'),
    path('dns/<int:entry_id>/', views.dnstest_detail, name='dnstest_detail'),
]
