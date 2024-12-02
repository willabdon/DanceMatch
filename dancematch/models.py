from django.db import models
from django.contrib.auth.models import User


class DanceStyle(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    

class Dancer(models.Model):
    BEGINNER = "beginner" 
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    
    LEVEL_CHOICES = (
        (BEGINNER, BEGINNER),
        (INTERMEDIATE, INTERMEDIATE),
        (ADVANCED, ADVANCED)
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    styles = models.ManyToManyField("DanceStyle")
    location = models.CharField(max_length=500)
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES)
