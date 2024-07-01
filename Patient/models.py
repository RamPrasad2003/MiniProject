from django.db import models
from django.contrib.auth.models import User
from main.models import CareTaker


class Patient(models.Model):
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    care=models.ForeignKey(CareTaker,null=True,on_delete=models.CASCADE)
    facial_image = models.ImageField(default='main\static\images\profile.png',upload_to='images')
    contact=models.CharField(null=True,unique=True,max_length=13)
    gender=models.CharField(null=True,max_length=6)
    dob=models.DateField(null=True)
    def __str__(self):
        return self.user.username

class Person(models.Model):
    patient=models.ForeignKey(Patient,null=True,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,null=True)
    dob=models.DateField(null=True)
    gender = models.CharField(max_length=6,null=True)
    relation = models.CharField(max_length=30,null=True)
    description = models.TextField(null=True)
    facial_image = models.ImageField(default='main\static\images\profile.png', upload_to='images')
    facial_embedding = models.BinaryField(null=True)
    def __str__(self):
        return self.name


class Medicine(models.Model):
    id = models.AutoField(primary_key=True)
    patient=models.ForeignKey(Patient,null=True,on_delete=models.CASCADE)
    name=models.TextField(max_length=50,null=True)
    dosage=models.TextField(max_length=50,null=True)
    time=models.TimeField(null=True)
    def __str__(self):
        return self.name


class Location(models.Model):
    patient=models.ForeignKey(Patient,null=True,on_delete=models.CASCADE)
    latitude=models.TextField(max_length=20,null=True)
    longitude=models.TextField(max_length=20,null=True)
    def __str__(self):
        return self.patient.user.username
