from django.db import models



# Create your models here.
class Role(models.Model):
    name=models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Userinfo(models.Model):
    user=models.CharField(max_length=32)
    email=models.EmailField()

    def __str__(self):
        return self.user

