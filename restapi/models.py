from django.db import models


class Group(models.Model):
    field = models.CharField(max_length=2)
    first_year = models.IntegerField()
    number = models.IntegerField()
    index = models.CharField(blank=True, primary_key=True, max_length=6)

    def __str__(self):
        return self.index

    def save(self, *args, **kwargs):
        field = self.field.upper()
        self.index = field+str(self.first_year)+'-'+str(self.number)
        super(Group, self).save(*args, **kwargs)


class Profile(models.Model):
    name = models.CharField(max_length=128)
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    is_monitor = models.BooleanField(default=False)
    hash = models.CharField(max_length=64, blank=True, unique=True)

    def save(self, *args, **kwargs):
        from hashlib import sha256
        self.hash = sha256((self.name+self.group.index).encode()).hexdigest()
        super(Profile, self).save(*args, **kwargs)


class HomeTask(models.Model):
    subject = models.CharField(max_length=128)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    deadline = models.DateField()
    task = models.TextField()
