from django.urls import path

from monitor import views

app_name = 'monitor'

urlpatterns = [
    path('', views.index, name='index'),
    path('device/<int:device_id>/', views.device_edit, name='device_edit'),
    path('scan/start/', views.scan_start, name='scan_start'),
    path('scan/<int:device_id>/', views.scan_details, name='scan_details'),
]
