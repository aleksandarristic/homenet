from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('dashboard.urls', namespace='dashboard')),
    path('runner/', include('runner.urls', namespace='runner')),
    path('djangoadmin/', admin.site.urls),
]
