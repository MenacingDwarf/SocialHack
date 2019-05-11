from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.courses, name='courses'),
    path('update/<int:id>/', views.update, name = 'update'),
    path('<int:id_course>/<int:id_lesson>/', views.lesson, name='lesson'),


]