from django.urls import path, register_converter

from common.url_converters import DateConverter
from dashboard import views

register_converter(DateConverter, 'date')
app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
]
