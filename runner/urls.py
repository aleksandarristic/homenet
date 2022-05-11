from django.urls import path

from runner import views

app_name = 'runner'

urlpatterns = [
    path('speedtest/', views.run_speedtest, name='run_command'),
]
