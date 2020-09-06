from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    field = models.CharField(max_length=2)
    first_year = models.IntegerField()
    number = models.IntegerField()
    index = models.CharField(blank=True, null=True, primary_key=True)

    def save(self, *args, **kwargs):
        field = self.field.upper()
        self.index = field+str(self.first_year)+'-'+str(self.number)
        super().save(*args, **kwargs)


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
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    task = models.TextField()
