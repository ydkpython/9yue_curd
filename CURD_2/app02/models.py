from django.db import models

# Create your models here.
class Myclass(models.Model):
    title=models.CharField(max_length=64)


class Youclass(models.Model):
    name=models.CharField(max_length=64)