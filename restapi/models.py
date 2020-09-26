from django.db import models


class Group(models.Model):
    field = models.CharField(max_length=2)
    first_year = models.IntegerField()
    number = models.IntegerField()
    index = models.CharField(blank=True, null=True, primary_key=True)

    def __str__(self):
        return self.index

    def save(self, *args, **kwargs):
        field = self.field.upper()
        self.index = field+str(self.first_year)+'-'+str(self.number)
        super().save(*args, **kwargs)


class Profile(models.Model):
    name = models.CharField(max_length=128)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL)
    is_monitor = models.BooleanField(default=False)


class HomeTask(models.Model):
    subject = models.CharField(max_length=128)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    deadline = models.DateField()
    task = models.TextField()
