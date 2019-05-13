from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.ForeignKey(User, models.CASCADE, default=1)
    name = models.CharField(max_length=30, blank=True)
    ava = models.CharField(max_length=100, default="https://cdn.pixabay.com/photo/2014/04/02/10/25/man-303792__340.png")
    second_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name + ' ' + self.second_name


class Teacher(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=30)
    ava = models.CharField(max_length=100, default="https://cdn.pixabay.com/photo/2014/04/02/10/25/man-303792__340.png")
    second_name = models.CharField(max_length=30)

    def __str__(self):
        return self.name + ' ' + self.second_name


class Course(models.Model):
    title = models.CharField(max_length=30)
    tutor = models.ForeignKey('Teacher', models.CASCADE, related_name="courses")

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=50)
    course = models.ForeignKey('Course', models.CASCADE, related_name="lessons")
    is_active = models.BooleanField(default=False)
    current_activity = models.ForeignKey('Activity', models.DO_NOTHING, default=None, blank=True, null=True, related_name="current_lessons")

    def __str__(self):
        return self.title


class Activity(models.Model):
    title = models.CharField(max_length=50)
    lesson = models.ForeignKey('Lesson', models.CASCADE, related_name="activities")
    answer = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Task(models.Model):
    activity = models.ForeignKey('Activity', models.CASCADE, related_name="tasks")
    type = models.SmallIntegerField()
    content = models.TextField()


class Answer(models.Model):
    task = models.ForeignKey('Task', models.CASCADE, related_name="answers")
    text = models.TextField()
    correct = models.BooleanField()
    students = models.ManyToManyField('Student', related_name='answers')


class StudentTask(models.Model):
    student = models.ForeignKey('Student', models.CASCADE)
    task = models.ForeignKey('Task', models.CASCADE)
    correctness = models.BooleanField()


class StudentCourse(models.Model):
    student = models.ForeignKey('Student', models.CASCADE)
    course = models.ForeignKey('Course', models.CASCADE)
    attendance = models.FloatField()
    correctness = models.FloatField()


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class DepartmentCourse(models.Model):
    course = models.ForeignKey('Course', models.CASCADE)
    department = models.ForeignKey('Department', models.CASCADE)
    coef = models.FloatField()
