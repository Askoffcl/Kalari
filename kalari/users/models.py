from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    name = models.CharField(max_length=100,null = True)
    role = models.CharField(max_length=20,default='admin')
    bio = models.CharField(max_length=200,null=True)
    exp = models.IntegerField(null=True)
    image = models.ImageField(upload_to='image/',null=True)
    phone = models.IntegerField(null=True)
    address=models.CharField(max_length=200,null=True)