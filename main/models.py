from django.db import models
from django.contrib.auth.models import User
### CREATING CARETAKER DB AND ITS SCHEMA
class CareTaker(models.Model):
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    contact=models.CharField(null=True,unique=True,max_length=13)
    facial_image = models.ImageField(default='main\static\images\profile.png',upload_to='images')
    gender = models.CharField(max_length=6,null=True)
    dob=models.DateField(null=True)
    def __str__(self):
        return self.user.username




