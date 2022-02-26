from rest_framework import serializers
from .models import BikeTrip

class BikeTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeTrip
        fields = ('__all__')
