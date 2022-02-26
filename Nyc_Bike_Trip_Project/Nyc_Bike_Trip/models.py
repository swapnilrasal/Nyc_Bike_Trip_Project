from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _


class BikeTrip(models.Model):
    genderChoice = (
            (0,"unknown"),(1,"male"),(2,"Female")
            )
    userTypeChoice = (
            ("Subscriber","Annual Member"),("Customer","24-hour pass or 3-day pass user")
            )

    id = models.AutoField(primary_key=True)
    trip_duration = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    stop_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    start_station_id = models.IntegerField(null=True, blank=True)
    start_station_name = models.CharField(max_length=100, null=True, blank=True)
    start_station_latitude = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    start_station_longitude = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    end_station_id = models.IntegerField(null=True, blank=True)
    end_station_name = models.CharField(max_length=100, null=True, blank=True)
    end_station_latitude = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    end_station_longitude = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    bikeid = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length = 1,choices=genderChoice, null=True, blank=True)
    user_type = models.CharField(max_length = 50,choices=userTypeChoice, null=True, blank=True)
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
