import logging
from rest_framework.generics import (ListAPIView,RetrieveAPIView)
from rest_framework.response import Response
from .models import BikeTrip
from .serializers import BikeTripSerializer
from Nyc_Bike_Trip_Project.custom_pagination import ListResultSetPagination
from Nyc_Bike_Trip_Project.helper_functions import distance, closest
from rest_framework import status
from rest_framework.schemas import AutoSchema
import coreapi
import decimal
import requests   


logger = logging.getLogger(__name__)

class BikeTripListAPIView(ListAPIView):
    """[BikeTrip List Api view.]
    """
    model = BikeTrip
    queryset = BikeTrip.objects.all().order_by("bikeid")
    serializer_class = BikeTripSerializer
    search_fields = (
        '^bikeid'
    )
    ordering_fields = (
        'started_at', 'ended_at', 'start_lat', 'start_lon', 'end_lat', 
        'end_lon'
    )
    pagination_class = ListResultSetPagination
    filter_fields = [
        'rideable_type', 'start_station_id','start_station_name', 'end_station_id',
        'end_station_name', 'member_casual']

    def get_queryset(self):
        if not self.request:
            return BikeTrip.objects.none()

        if self.request.query_params:
            queryset = self.filter_queryset(self.queryset)
        else:
            queryset = self.queryset

        return queryset

class GetSingleTripInstanceView(RetrieveAPIView):

    model = BikeTrip
    serializer_class = BikeTripSerializer
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field("bikeid",
                          required=True,
                          location='query',
                          description='trip bikeid'
                          )
        ]
    )

    def get(self, request, bikeid):
        """[Get specific trip]"""

        try:
            bike_trip_obj = BikeTrip.objects.filter(bikeid=bikeid).first()

        except BikeTrip.DoesNotExist:
            bike_trip_obj = None
            pass

        if bike_trip_obj:

            serializer_data = BikeTripSerializer(bike_trip_obj).data

            start_lat = abs(decimal.Decimal(serializer_data["start_lat"]).as_tuple().exponent)
            if start_lat > 4:
                serializer_data["start_lat"] = round(serializer_data["start_lat"], 4)

            start_lng = abs(decimal.Decimal(serializer_data["start_lon"]).as_tuple().exponent)
            if start_lng > 4:
                serializer_data["start_lon"] = round(serializer_data["start_lon"], 4)

            # ------------ Fetch Observation Station Data -------------------------
            api_url = f'https://api.weather.gov/points/{{latitude}},{{longitude}}'.format(
                latitude=serializer_data["start_lat"],
                longitude=serializer_data["start_lon"]
            )
            resp = requests.get(api_url)
            observation_api_resp = resp.json()
            # print(observation_api_resp)

            # ------------ Fetch List Of Station Data -------------------------
            observationStations = observation_api_resp["properties"]["observationStations"]
            list_stations_data = requests.get(observationStations)
            list_stations_resp = list_stations_data.json()
            # print(list_stations_resp)

            list_of_stations = []
            for fdata in list_stations_resp["features"]:
                station_obj ={
                    "id": fdata["id"],
                    "lat": fdata["geometry"]["coordinates"][1],
                    "lon": fdata["geometry"]["coordinates"][0]
                }
                list_of_stations.append(station_obj)

            # ------------ Find Nearest Coordinates Station -------------------------

            start_coordinates = {
                'lat': float(serializer_data["start_lat"]), 
                'lon': float(serializer_data["start_lon"])
                }
            closest_station_data = closest(list_of_stations, start_coordinates)
            # print(closest_station_data)

            # ------------ Fetch Weather Conditions Data -------------------------

            closest_station_url = closest_station_data["id"] + f'/observations?start={{started_at}}&limit=1'.format(
                started_at=serializer_data["started_at"]
            )
            weather_data = requests.get(closest_station_url)
            weather_data_json = weather_data.json()

            serializer_data["weather_conditions"] = weather_data_json["features"][0]["properties"]["textDescription"]
            serializer_data["temperature"] = weather_data_json["features"][0]["properties"]["temperature"]["value"]

            return Response({
                'success': True,
                'msg': "Record Fetched Successfully" ,
                "data": serializer_data,
                "status": status.HTTP_200_OK
            })
        else:
            return Response("Record Not Found",
                            status=status.HTTP_400_BAD_REQUEST)

