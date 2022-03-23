from django.urls import path

from monitor import views

app_name = 'monitor'

urlpatterns = [
    path('', views.device_day, name='index'),
    path('device/all/', views.device_all, name='device_all'),
    path('device/<date:day>/', views.device_day, name='device_day'),
    path('device/filter/', views.device_filter, name='device_filter'),
    path('device/<int:device_id>/', views.device_details, name='device_details'),
    path('device/edit/<int:device_id>/', views.device_edit, name='device_edit'),
    path('device/history/<int:device_id>/', views.device_history, name='device_history'),
    path('scan/start/', views.scan_start, name='scan_start'),
    path('scan/<int:device_id>/', views.scan_details, name='scan_details'),
]
