from struct import pack
from django.db import models

# Create your models here.
class Admin(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=20)
    def __str__(self):
       return self.username

class Userdata(models.Model):
    id=models.BigAutoField(primary_key=True)
    uname=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobileno=models.CharField(max_length=12)
    password=models.CharField(max_length=30)

    def __str__(self):
        return self.email
    
class Pack(models.Model):
    packname=models.CharField(max_length=100)
    pack_type=models.CharField(max_length=50)
    price=models.IntegerField()
    
    def __str__(self):
        return self.packname
    
class Combo(models.Model):
    packname=models.ForeignKey(Pack,on_delete=models.CASCADE)
    channelname=models.CharField(max_length=20)
    channellang=models.CharField(max_length=20)
    channeldes=models.CharField(max_length=20)
    channelamount=models.IntegerField()
    channeltype=models.CharField(max_length=20)
    channelty=models.CharField(max_length=20)

    def __str__(self):
        return self.channelname
    
class User_pack(models.Model):
    email=models.ForeignKey(Userdata,on_delete=models.CASCADE)
    packname=models.ForeignKey(Pack,on_delete=models.CASCADE)
    user_id=models.IntegerField()
    pack_status=models.CharField(max_length=50)
    datef=models.DateField()
    enddat=models.DateField()
    days_remaining=models.IntegerField()

    
    