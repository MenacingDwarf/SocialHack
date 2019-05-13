from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.Course)
admin.site.register(models.StudentCourse)
admin.site.register(models.Lesson)
admin.site.register(models.Activity)
admin.site.register(models.Task)
admin.site.register(models.Answer)
admin.site.register(models.StudentTask)
admin.site.register(models.Department)
admin.site.register(models.DepartmentCourse)
