                    ######      VIEWS OF PATIENT ######

### IMPORTING THE LIBRARIES 
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,login,logout
from datetime import *
from main.models import *
from sklearn.svm import SVC
import cv2
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import mtcnn
import json
import mtcnn
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import os

### MAKING MTCNN MODEL 
detector=mtcnn.MTCNN()
mtcnn1 = MTCNN()

### MAKING IRV1 PRETRAINED VGGFACE2 OR WE CAN USE CASIAWEBFACE 
resnet = InceptionResnetV1(pretrained='vggface2').eval()  

### MAKING SVC MODEL
model=SVC(probability=True)

### DISPLAY THE PROFILE DETAILS OF THE PATIENT
def patientprofile(request):
    if not request.user.is_authenticated:
        return redirect('patientlogin')
    error=False
    user=User.objects.get(id=request.user.id)
    data=Patient.objects.get(user=user)
    d={'d':data,'user':user}
    return render(request,'patientprofile.html',d)
### DISPLAY THE PERSONS DETAILS WHO ARE ADDED FOR FACE RECOGNITION FOR A PARTICULAR USER
def mypersons(request):
    if not request.user.is_authenticated:
        return redirect('patientlogin')
    error=False
    patient=request.user.id
    p=Patient.objects.get(user=patient)
    user=Person.objects.filter(patient=p)
    d={'users':user}
    return render(request,'mypersons.html',d)

### TRAINING THE SVC MODEL
def train(user):
    x=[]
    y=[]
    for i in user:
        x.append(np.frombuffer(i.facial_embedding, dtype=np.float32))
        y.append(i.id)
    model.fit(x,y)
    return model
detector=MTCNN()
### OPEN WEBCAM FOR FACE RECOGNITION
@csrf_exempt
def scan(request):
    if not request.user.is_authenticated:
        return redirect('patientlogin')
    patient=request.user.id
    p=Patient.objects.get(user=patient)
    user=Person.objects.filter(patient=p)
    model=train(user)
    return render(request,'scan.html')
### ALLOWS TO EDIT THE PROFILE OF THE PATIENT 
def profileEdit(request):
    if not request.user.is_authenticated:
        return redirect('patientlogin')
    error=False
    user=User.objects.get(id=request.user.id)
    data=Patient.objects.get(user=user)
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        c=request.POST['con']
        gender=request.POST['gender']
        dob=request.POST['dob']
        user.first_name=f
        user.last_name=l
        data.contact=c
        data.gender=gender
        data.dob=dob
        user.save()
        data.save()
        error=True
    d={'data':data,'user':user,'error':error}
    return render(request,'patproedit.html',d)
### CHANGE PASSWORD FUNCTION FOR PATIENT
def changpass(request):
    error=""
    if not request.user.is_authenticated:
        return redirect('patientlogin')
    if request.POST:
        old=request.POST['old']
        new=request.POST['new']
        confirm=request.POST['confirm']
        if confirm==new:
            u=User.objects.get(username__exact=request.user.username)
            u.set_password(new)
            u.save()
            error='no'
        else:
            error='yes'
    d={'error':error}
    return render(request,'changpass.html',d)
### API CALL FOR FACE RECOGNITION TAKEN FOR SCAN PAGE 
@csrf_exempt
def detect_faces(request):
    if not request.user.is_authenticated:
        return redirect('patientlogin')
    data={'user':'UNKNOWN'}
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        image_data = json_data['image']
        encoded_data = image_data.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        result = mtcnn.MTCNN().detect_faces(image)
        print('njdd',result)
        patient=request.user.id
        p=Patient.objects.get(user=patient)
        user=Person.objects.filter(patient=p)
        for face in result:
            bounding_box = face['box']
            cv2.rectangle(image,
                          (bounding_box[0], bounding_box[1]),
                          (bounding_box[0]+bounding_box[2], bounding_box[1]+bounding_box[3]),
                          (0, 255, 0),
                          2)
            aligned1 = detector(image)
            if aligned1 is not None:
                aligned1 = aligned1.unsqueeze(0) 
                print(aligned1.shape)
                embeddings1 = resnet(aligned1).detach()
                x=[]
                for i in user:
                    x.append(np.frombuffer(i.facial_embedding, dtype=np.float32))
                distances = np.linalg.norm( np.array(x)- np.array(embeddings1))
                threshold = 2.4
                ### THRESHOLDING 
                print(distances)
                if distances < threshold:
                    id=model.predict(embeddings1)
                    user=Person.objects.get(id=id)
                    data = {
                        'name':user.name,
                        'relation':user.relation,
                        'description':user.description,
                        'gender':user.gender
                    }
                else:
                    data={}
        return JsonResponse({'image': data})  # Sending back the image data
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
### OPEN MAPS PAGE 
def location(request):
    if not request.user.is_authenticated:
        return redirect('patientlogin')
    return render(request,'mylocation.html')
### COLLECTS LAT,LONG DATA AND MEDICINE REMAINDER IS DONE 
@csrf_exempt
def nav_data(request):
    if not request.user.is_authenticated:
        return redirect('patientlogin')
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        lat = json_data['latitude']
        lng = json_data['longitude']
        p=Patient.objects.get(user=request.user.id)
        Location.objects.create(latitude=lat,longitude=lng,patient=p)
        med=Medicine.objects.filter(patient=p)
        l=[]
        cur=datetime.now()
        ft = cur.strftime("%H:%M")
        if ft=="23:59" or ft=="11:59":
            truncate_location()
            print('turncated')
        for i in med:
            t=i.time.strftime("%H:%M")
            cur=datetime.now()
            ft = cur.strftime("%H:%M")
            if t==ft:
                a='Time for '+i.name+' with dosage of '+i.dosage
                l.append(a)
        return JsonResponse({'message':l})
    return JsonResponse({'message':l})

### DISPLAYS THE MEDICINE DETAILS OF A PARTICULAR PATIENT 
def medicine(request):
    if not request.user.is_authenticated:
        return redirect('patientlogin')
    p=Patient.objects.get(user=request.user.id)
    med=Medicine.objects.filter(patient=p)
    d={'med':med}
    return render(request,'medicine.html',d)
### ALL THE LAT,LONG POINTS OF THE PATIENT 
@csrf_exempt
def get_loc(request):
    if not request.user.is_authenticated:
        return redirect('patientlogin')
    if request.method=='POST':
        d=[]
        p=Patient.objects.get(user=request.user.id)
        l=Location.objects.filter(patient=p)
        for i in l:
            d.append([i.latitude,i.longitude])
        data={'list':d}
        return JsonResponse(data)
### TRUNCATE THE LOCATION DATABASE TABLE 
def truncate_location():
    Location.objects.all().delete()
### PATIENT HOME PAGE
def patienthome(request):
    if not request.user.is_authenticated:
        return redirect('patientlogin')
    return render(request,'patienthome.html')