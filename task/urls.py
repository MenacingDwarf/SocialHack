from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.courses, name='courses'),
    path('update/<int:id>/', views.update, name = 'update'),
    path('<int:id_course>/<int:id_lesson>/', views.lesson, name='lesson'),
    path('<int:id_course>/<int:id_lesson>/update/present/', views.present, name='present'),
    path('<int:id_course>/<int:id_lesson>/update/task/', views.task, name='task'),



]