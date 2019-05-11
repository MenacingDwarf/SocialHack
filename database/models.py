from django.db import models


class Student(models.Model):
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.id
