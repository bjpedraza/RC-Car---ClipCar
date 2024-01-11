from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import  settings

urlpatterns = [
    path('', views.home, name='home'),
    path('videos/', views.displayVideos, name='videos'),
    path('upload/', views.uploadVideo, name='upload'),
    path('controlMotor', views.controlMotor, name='controlMotor'),
    path('record', views.record, name='record'),
    #path('file_upload/', views.record, name='record'),
    #path('record_status/', views.record_status, name='record_status'),
    path('videoFeed', views.videoFeed, name='videoFeed')
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
