from django.db import models


class OZFeature(models.Model):
    worldid = models.CharField(max_length=30)
    zonename = models.CharField(max_length=100)
    cntyid = models.CharField(max_length=5)
    cntyname = models.CharField(max_length=30)
    globalid = models.CharField(max_length=50)
    population = models.IntegerField()
    cen_x = models.FloatField()
    cen_y = models.FloatField()
    labelname = models.CharField(max_length=100)
    polygons = models.TextField()
    




    


    
    

     
    


