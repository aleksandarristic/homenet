from django.urls import path

from monitor import views

app_name = 'monitor'

urlpatterns = [
    path('', views.device_day, name='index'),
    path('devices/<date:day>/', views.device_day, name='device_day'),
    path('device/filter/', views.device_filter, name='device_filter'),
    path('device/<int:device_id>/', views.device_edit, name='device_edit'),
    path('scan/start/', views.scan_start, name='scan_start'),
    path('scan/<int:device_id>/', views.scan_details, name='scan_details'),
]
