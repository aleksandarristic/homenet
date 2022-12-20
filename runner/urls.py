from django.urls import path

from runner import views

app_name = 'runner'

urlpatterns = [
    path('speedtest/', views.run_speedtest, name='run_speedtest'),
    path('ping/', views.run_ping, name='run_ping'),
]
