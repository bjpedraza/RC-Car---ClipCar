from django.db import models
#from datetime import datetime
from django.utils.timezone import now

# Create your models here.
class Videos(models.Model):
    title = models.CharField(max_length=100)
    #date = models.DateTimeField(default=now, blank=True)
    video = models.FileField(upload_to='videos/')
    
    
    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'
        
    def __str__(self):
        return self.title