from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.http import StreamingHttpResponse
from django.core import serializers
from .stream import VideoCamera
from .models import Videos
import RPi.GPIO as GPIO
import time
import threading
import os
import json

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#camera = VideoCamera() # flip pi camera if upside down.
#camera = picamera.PiCamera()

#from .models import Videos

recStop = 1

video_camera = None
global_frame = None

status = 0;

PWM0_pin = 32
PWM1_pin = 33
Motor1_a = 16
Motor1_b = 18
Motor2_a = 11
Motor2_b = 13

GPIO.setup(PWM0_pin, GPIO.OUT)
GPIO.setup(PWM1_pin, GPIO.OUT)
GPIO.setup(Motor1_a, GPIO.OUT)
GPIO.setup(Motor1_b, GPIO.OUT)
GPIO.setup(Motor2_a, GPIO.OUT)
GPIO.setup(Motor2_b, GPIO.OUT)

#creat a PWM instance p and pass the pin num. and frequency as parameters
p0 = GPIO.PWM(PWM0_pin,100)
p1 = GPIO.PWM(PWM1_pin,100)

duty0 = 0;
duty1 = 0;
p0.ChangeDutyCycle(0)
p1.ChangeDutyCycle(0)
GPIO.output(Motor1_a, GPIO.LOW)
GPIO.output(Motor1_b, GPIO.LOW)
GPIO.output(Motor2_a, GPIO.LOW)
GPIO.output(Motor2_b, GPIO.LOW)



# Create your views here.
def home(request):      
    return render(request, 'index.html')


def record_status(status):
    global video_camera
    if video_camera == None:
        video_camera = VideoCamera()

    #status = request.POST.get(record);
    #Req = json.loads(request.body)
    #video_camera.stop_record()
    #status = json['status']
    print(status)
    
    if status == '1':
        video_camera.start_record()
        #return JsonResponse({ 'status':True})
    else:
        video_camera.stop_record()
        #return JsonResponse({'status': False})


def gen():    
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        #video_camera.start_record()
        
    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')
        
        
def videoFeed(request):
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')


def uploadVideo(request):  
    if request.method == 'POST':
        title = request.POST['title']
        video = request.POST['video']
        
        content = Videos(title=title,video=video)
        content.save()
        return redirect('home')
    
    return render(request,'upload.html')

'''
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def file_upload(request):
    if request.method == 'POST':
        video = request.FILES['video.mp4']
        form = Videos(title="TEST", video=video)
        form.save
        return redirect('home')
    else:
        form = Videos()
    return render(request,'home.html')


def file_upload(request):
    if request.method == 'POST':
        form = Videos(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data.get('video.mp4')
            file_bytes = file.read()
            a = File.objects.create(du_file = file_bytes ,du_file_name=file_name,du_file_extension=extension,
            du_file_size='1023') 

            a.save()

            return HttpResponse(file_name)
        else:
            return HttpResponse('Form is not valid!')
    else:
        return HttpResponse('Failed') 


def file_upload(request):
    save_path = os.path.join(settings.MEDIA_ROOT, 'media', request.FILES['video.mp4'])
    path = default_storage.save(save_path, request.FILES['video.mp4'])
    default_storage.path(path)
    
    return redirect('home')
'''


def record(request):
    if request.is_ajax and request.method == 'GET':
        recStart = request.GET.get('rec')
        return JsonResponse({ })


def displayVideos(request):
    videos = Videos.objects.all()
    context ={
        'videos':videos,
    }

    return render(request, 'videos.html', context)
# after pasinng it in thru html, to use the passed data is {{myVideos.folder.url}}


def controlMotor(request):
    if request.is_ajax and request.method == 'POST':
        global recStop
        valx = request.POST.get('stick1_x')
        valy = request.POST.get('stick1_y')
        status = request.POST.get('record')
        
        if(status == '1' and recStop == 1):
            record_status(status)
            recStop = 0
        elif(status == '0' and recStop == 0):
            record_status(status)
            recStop = 1
        
        print('x = ', valx);
        print('y = ', valy);
        
        #Forward
        if(float(valy) > 0):
            GPIO.output(Motor1_a, GPIO.HIGH)
            GPIO.output(Motor1_b, GPIO.LOW)

        elif(float(valy) < 0):
            GPIO.output(Motor1_a, GPIO.LOW)
            GPIO.output(Motor1_b, GPIO.HIGH)

        else:
            GPIO.output(Motor1_a, GPIO.LOW)
            GPIO.output(Motor1_b, GPIO.LOW)

        #p0.start(duty0)
        #p0.ChangeDutyCycle(float(valy)*100);
        #p0.stop()

    
        return JsonResponse({'status' : 1})#json.dumps(camera.get_frame())})
    
    return JsonResponse({'status' : 0})
