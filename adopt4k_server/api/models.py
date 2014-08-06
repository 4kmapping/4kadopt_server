from django.db import models
from django.contrib.auth.models import User


class OZFeature(models.Model):
    worldid = models.CharField(max_length=30, unique=True)
    zonename = models.CharField(max_length=100)
    world_type = models.CharField(max_length=1)
    cntyid = models.CharField(max_length=5)
    cntyname = models.CharField(max_length=100)
    globalid = models.CharField(max_length=50)
    population = models.IntegerField()
    cen_x = models.FloatField()
    cen_y = models.FloatField()
    labelname = models.CharField(max_length=100)
    polygons = models.TextField()
    

class Adoption(models.Model):
    worldid = models.CharField(max_length=30, unique=True)
    targetyear = models.IntegerField()
    user = models.ForeignKey(User)
    update = models.DateTimeField(auto_now=True)
    is_adopted = models.BooleanField()
    
     


    


    
    

     
    


