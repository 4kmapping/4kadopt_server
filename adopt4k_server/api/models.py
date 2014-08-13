from django.db import models
from django.contrib.auth.models import User
import os

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
    worldid = models.CharField(max_length=30)
    targetyear = models.IntegerField()
    user = models.ForeignKey(User)
    update = models.DateTimeField(auto_now=True)
    is_adopted = models.BooleanField()
    # Additional info to display
    oz_zone_name = models.CharField(max_length=50)
    oz_country_name = models.CharField(max_length=50)
    user_display_name = models.CharField(max_length=50) 
    

    def save(self, *args, **kwargs):
        super(Adoption, self).save(*args, **kwargs)

        # super hacky, but its fast
        isUpdatedFilePath = os.path.dirname(os.path.realpath(__file__)) + "/../../isUpdated.txt"
        #isUpdatedFile = UPDATE_FILE_LOC
        isUpdatedFile = open(isUpdatedFilePath, 'w')
        isUpdatedFile.write("11")
        isUpdatedFile.close()

    class Meta:
        unique_together = ('worldid','user')