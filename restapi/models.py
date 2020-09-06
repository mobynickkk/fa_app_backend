from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField()
    name = models.CharField(max_length=128)
    faculty = models.CharField(max_length=32)
    group = models.CharField(max_length=8)
    is_monitor = models.BooleanField(default=False)


class Subject(models.Model):
    name = models.CharField(max_length=32)
    department = models.CharField(max_length=32)


class HomeTask(models.Model):
    pass
