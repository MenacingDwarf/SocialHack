from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('log/', views.log, name='log'),
    path('push/<int:id>/', views.push, name='push'),
    path('add/', views.add, name='add'),
    path('out/', views.out, name='out'),
    path('option/', views.option, name='option'),
    path('statistic/<int:id>', views.statistic, name='statistic')
]