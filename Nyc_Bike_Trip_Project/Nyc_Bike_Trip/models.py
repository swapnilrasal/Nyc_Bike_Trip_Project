from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _


class BikeTrip(models.Model):
    memberTypeChoice = (
            ("casual","casual"),("Customer","member")
            )

    bikeid = models.CharField(max_length=50, primary_key=True)
    rideable_type = models.CharField(max_length=50, null=True, blank=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    start_station_id = models.CharField(max_length=50, null=True, blank=True)
    start_station_name = models.CharField(max_length=100, null=True, blank=True)
    end_station_id = models.CharField(max_length=50, null=True, blank=True)
    end_station_name = models.CharField(max_length=100, null=True, blank=True)
    start_lat = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    start_lon = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    end_lat = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    end_lon = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    member_casual = models.CharField(max_length = 50,choices=memberTypeChoice, null=True, blank=True)
