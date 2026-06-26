from django.db import models

# Create your models here.
class Admin_login(models.Model):
    email=models.CharField(max_length=200,primary_key=True)
    password=models.CharField(max_length=120,null=True)

    def __str__(self):
        return self.email



class Addi_staff(models.Model):
    username=models.CharField(max_length=200,null=False)
    email=models.CharField(max_length=200,null=False,primary_key=True)
    password=models.CharField(max_length=120,null=False)

    def _str__(self):
        return self.username


class upload_templates(models.Model):
    image1=models.ImageField(upload_to="Uploads/")
    image2=models.ImageField(upload_to="Uploads/")
    image3=models.ImageField(upload_to="Uploads/")
    price=models.IntegerField()
    description=models.CharField(max_length=200,null=True)
    item_name=models.CharField(max_length=200)

    def _str__(self):
        return self.description




