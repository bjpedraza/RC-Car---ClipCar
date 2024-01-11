import cv2
#from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
import threading
import os
from .models import Videos
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

from pathlib import Path
from IPython.display import FileLink
from django.core.files.base import ContentFile
from moviepy.editor import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

count = 0;
fileName = ""

class RecordingThread (threading.Thread):
    def __init__(self, name, camera):
        global count
        global fileNname
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        fileName = "media/video" + str(count) + ".avi"
        self.out = cv2.VideoWriter(fileName,fourcc, 15.0, (640,480))
        count = 1 + count

    def run(self):
        global fileName
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)

        self.out.release()
        
        
        #HERE, The Record video is done NOW time SAVE to database please!
        '''
        #clip = VideoFileClip(fileName)
        fs = FileSystemStorage(location='media/video.mp4')
        photo = models.FileField(storage=fs)
        
        content = Videos(title="wow",video=photo)
        content.save()
        '''
        '''
        with open(BASE_DIR / 'media/video.mp4', 'rb+') as rf:
            #file_link = FileLink(path=' media/video.mp4')
            content = Videos()
            
            chunk_size = 4096
            rf_chunk = rf.read(chunk_size)
            while len(rf_chunk) > 0:
                content.video += rf_chunk
                rf_chunk = rf.read(chunk_size)
                
                content.title = 'sux';
                print(content.title)
            #content.save()
            #cap.release()
        '''
        #content = Videos()
        #fs = FileSystemStorage(location='/media/video.mp4')
        #files =  request.FILES[
        #content.video = models.FileField(storage=fs)
        #content.title = 'wow'
        #content.save()
        

    def stop(self):
        self.isRunning = False
        #self.out.release()

    def __del__(self):
        self.out.release()


class VideoCamera(object):
    def __init__(self, flip = False):
        #self.cap = PiVideoStream(resolution=(852, 480), framerate=32).start()
        self.cap = cv2.VideoCapture(0);
        self.cap.set(3,640)
        self.cap.set(4,480) 
        #self.width = int(self.cap.get(3))
        #self.height = int(self.cap.get(4))
        #self.size = (self.width, self.height)
        #self.out = cv2.VideoWriter("output.mp4", camera.fourcc, 20, camera.size)
        
        self.is_record = False
        self.out = None
        self.recordingThread = None
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.cap.release()
        #self.out.release()
        #cv2.destroyAllWindows()

    def get_frame(self):
        ret, frame = self.cap.read()        
        ret, jpeg = cv2.imencode('.jpg', frame)
        
        #Record video
        #if self.is_record:
        #    if self.out == None:
        #        fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        #        self.out = cv2.VideoWriter('media/examplevideo.avi',fourcc, 20.0, (640,480))
                #ret, jpeg = cv2.imencode('.jpg', frame)
            
        #    self.out.write(frame)
        #elif self.is_record == False and self.out != None:
        #    self.out.release()
        #    self.out = None
        
        return jpeg.tobytes()
        

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False
        
        if self.recordingThread != None:
            self.recordingThread.stop()
    
    
