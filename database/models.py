from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.ForeignKey(User, models.CASCADE, default=1)
    name = models.CharField(max_length=30, blank=True)
    second_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name+' '+self.second_name


class Teacher(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)

    def __str__(self):
        return self.name+' '+self.second_name


class Course(models.Model):
    title = models.CharField(max_length=30)
    tutor = models.ForeignKey('Teacher', models.CASCADE, related_name="courses")

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=50)
    course = models.ForeignKey('Course', models.CASCADE, related_name="lessons")

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


class StudentTask(models.Model):
    student = models.ForeignKey('Student', models.CASCADE)
    task = models.ForeignKey('Task', models.CASCADE)
    correctness = models.BooleanField()


class StudentCourse(models.Model):
    student = models.ForeignKey('Student', models.CASCADE)
    course = models.ForeignKey('Course', models.CASCADE)
    attendance = models.FloatField()
    correctness = models.FloatField()


