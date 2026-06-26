from django.db import models

# Create your models here.
class Staff_reg(models.Model):
    username=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    status=models.IntegerField()
