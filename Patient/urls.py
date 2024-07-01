from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path("patientprofile",patientprofile,name='patientprofile'),
    path("mypersons",mypersons,name='mypersons'),
    path("scan",scan,name='scan'),
    path('profileEdit', profileEdit, name='profileEdit'),
    path('changpass', changpass, name='changpass'),
    path('detect_faces', detect_faces, name='detect_faces'),
    path('get_loc', get_loc, name='get_loc'),
    path('nav_data', nav_data, name='nav_data'),
    path('location', location, name='location'),
    path('medicine', medicine, name='medicine'),
    path('patienthome', patienthome, name='patienthome'),
]