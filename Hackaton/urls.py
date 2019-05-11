from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('start.urls')),
    path('courses/', include('task.urls')),

    path('front/', include('frontApp.urls')),
]
