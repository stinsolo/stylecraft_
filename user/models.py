from django.db import models
from Admin.models import*
from staff.models import*

# Create your models here.

class User_Reg(models.Model):
    username=models.CharField(max_length=200,null=False)
    email=models.CharField(max_length=200,null=False,primary_key=True)
    password=models.CharField(max_length=200,null=False)
    address=models.CharField(max_length=200,null=False)
    gender=models.IntegerField(default=0) #1 for male 0 for female


class Upload_details(models.Model):
    username=models.ForeignKey(User_Reg,on_delete=models.CASCADE)
    waist=models.IntegerField(null=False)
    hips=models.IntegerField(null=False)
    bust=models.IntegerField(null=False)
    chestgirth=models.IntegerField(null=False)
    neck=models.IntegerField(null=False)
    shoulder=models.IntegerField(null=False)
    sleeve=models.IntegerField(null=False)
    bicep=models.IntegerField(null=False)
    wrist=models.IntegerField(null=False)
    back_waist_length=models.IntegerField(null=False)


class Order_table(models.Model):
    item_name=models.ForeignKey(upload_templates,null=True ,blank=True,on_delete=models.CASCADE)
    status=models.IntegerField(default=0)
    make_sts=models.IntegerField(default=0)
    username=models.ForeignKey(User_Reg,on_delete=models.CASCADE)
    image1=models.ImageField(upload_to="")
    image2=models.ImageField(upload_to="")
    image3=models.ImageField(upload_to="")
    waist=models.IntegerField(null=False)
    hips=models.IntegerField(null=False)
    bust=models.IntegerField(null=False)
    chestgirth=models.IntegerField(null=False)
    neck=models.IntegerField(null=False)
    shoulder=models.IntegerField(null=False)
    sleeve=models.IntegerField(null=False)
    bicep=models.IntegerField(null=False)
    wrist=models.IntegerField(null=False)
    back_waist_length=models.IntegerField(null=False)

    def __str__(self):
        return self.username

class OrderStatus(models.Model):
    order=models.ForeignKey(Order_table,on_delete=models.CASCADE)
    status=models.IntegerField(default=0) # 0 order placed, 1 accepted oder , 2- payment done , 3- product done , 4- product shipped , 5- delivered 
    staff=models.ForeignKey(Staff_reg,on_delete=models.CASCADE,null=True)
    rate=models.FloatField(null=True)





class feed_back(models.Model):
    username=models.CharField(max_length=200,null=False)
    text=models.CharField(max_length=400,null=False)

    def __str__(self):
        return self.text



    

