from django.db import models

class BikeTrip(models.Model):
    tripduration = models.IntegerField()
    starttime = models.DateTimeField(auto_now_add=True)
    stoptime = models.DateTimeField(auto_now_add=True)
