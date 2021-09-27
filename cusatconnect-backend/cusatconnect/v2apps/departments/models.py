from django.db import models


class Stream(models.Model):
    stream_name = models.CharField(max_length=200)
    department_name = models.ManyToManyField('Department')

    def __str__(self):
        return self.stream_name


class Department(models.Model):
    department_name = models.CharField(max_length=200)

    def __str__(self):
        return self.department_name
