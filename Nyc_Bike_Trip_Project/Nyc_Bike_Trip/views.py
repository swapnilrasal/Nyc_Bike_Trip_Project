import logging
from rest_framework.generics import (ListAPIView)
# from rest_framework.response import Response
from .models import BikeTrip
from .serializers import BikeTripSerializer
from Nyc_Bike_Trip_Project.custom_pagination import ListResultSetPagination


logger = logging.getLogger(__name__)

class BikeTripListAPIView(ListAPIView):
    """[BikeTrip List Api view.]
    """
    model = BikeTrip
    queryset = BikeTrip.objects.all()
    serializer_class = BikeTripSerializer
    pagination_class = ListResultSetPagination
    filter_fields = [
        'trip_duration', 'start_time', 'stop_time', 'start_station_latitude',
        'start_station_id','start_station_name', 'end_station_id',
        'start_station_longitude', 'end_station_latitude', 'end_station_longitude',
        'end_station_name','bikeid', 'gender', 'user_type', 'birth_year']

    def get_serializer_context(self):
        return {'request': self.request}
