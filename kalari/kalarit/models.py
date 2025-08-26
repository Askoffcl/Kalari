from pickle import TRUE
from pyexpat import model
from tkinter import CASCADE
from turtle import mode
from django.db import models
from users.models import User

class Class(models.Model):
    name = models.CharField(max_length=100,null=True)
    teacher = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField()
    duration = models.IntegerField(null=True)
    desc = models.CharField(max_length=100,null = True)
    image = models.ImageField(upload_to='image/',null=True)
    amount = models.IntegerField(null=True)


class Events(models.Model):
    name = models.CharField(max_length=100,null = True)
    date = models.DateField()
    loc = models.CharField(max_length=100,null = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    desc =models.CharField(max_length=200,null = True)
    image = models.ImageField(upload_to='image/',null=True)
    amount = models.IntegerField(null=True)


class Training(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null = True)
    title = models.CharField(max_length=100)
    desc = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='materials/')  # stores files inside MEDIA_ROOT/materials/
    uploaded_at = models.DateTimeField(auto_now_add=True)


class EnrollClass(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    classid = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    ATTENDANCE_CHOICES = [
        ('Not Started', 'Not Started'),
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    attend = models.CharField(
        max_length=100,
        choices=ATTENDANCE_CHOICES,
        default='Not Started',
        null=True
    )

class Feedback(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    class_attended = models.ForeignKey(EnrollClass, on_delete=models.SET_NULL, null=True)
    attended_date = models.DateField(null=True, blank=True)
    rating = models.IntegerField(null=True)
    comment = models.CharField(max_length=200, null=True)
    reply = models.CharField(max_length=200,null=TRUE)
    reply_at = models.DateTimeField(null=True, blank=True)




  
class EnrollEvent(models.Model):
    pid = models.ForeignKey('kalarit.Payment',on_delete=models.CASCADE,null=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    eventid = models.ForeignKey(Events,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True)
  

class Payment(models.Model):
    name =  models.CharField(max_length=200,null=True)
    cardnumber = models.IntegerField(null = True)
    cvv = models.IntegerField(null =True)
    date = models.DateTimeField(null= True)
    method = models.CharField(max_length=200,null=True)
    classid = models.ForeignKey(Class,on_delete=models.CASCADE,null=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    eventid = models.ForeignKey(Events,on_delete=models.CASCADE,null=True)
    amount = models.IntegerField(null=True)
    def __str__(self):
        return f"{self.method} - {self.name}" if self.method else "No Payment Method"
    


class ChatMessage(models.Model):
    classid = models.ForeignKey('Class', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} - {self.message[:20]}"