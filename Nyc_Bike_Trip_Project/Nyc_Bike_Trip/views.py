import logging
from rest_framework.generics import (ListAPIView)
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

class GetSingleTripInstanceView(ListAPIView):

    model = BikeTrip
    serializer_class = BikeTripSerializer
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field("id",
                          required=True,
                          location='query',
                          description='trip id'
                          )
        ]
    )

    def get(self, request, id):
        """[Get specific trip]"""
        try:
            bike_trip_obj = BikeTrip.objects.get(
                id=id
            )
        except BikeTrip.DoesNotExist:
            bike_trip_obj = None
            pass

        if bike_trip_obj:

            serializer_data = BikeTripSerializer(bike_trip_obj).data

            start_lat = abs(decimal.Decimal(serializer_data["start_station_latitude"]).as_tuple().exponent)
            if start_lat > 4:
                serializer_data["start_station_latitude"] = round(serializer_data["start_station_latitude"], 4)

            start_lng = abs(decimal.Decimal(serializer_data["start_station_longitude"]).as_tuple().exponent)
            if start_lng > 4:
                serializer_data["start_station_longitude"] = round(serializer_data["start_station_longitude"], 4)

            # ------------ Fetch Observation Station Data -------------------------
            api_url = f'https://api.weather.gov/points/{{latitude}},{{longitude}}'.format(
                latitude=serializer_data["start_station_latitude"],
                longitude=serializer_data["start_station_longitude"]
            )
            resp = requests.get(api_url)
            observation_api_resp = resp.json()

            # ------------ Fetch List Of Station Data -------------------------
            observationStations = observation_api_resp["properties"]["observationStations"]
            list_stations_data = requests.get(observationStations)
            list_stations_resp = list_stations_data.json()

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
                'lat': float(serializer_data["start_station_latitude"]), 
                'lon': float(serializer_data["start_station_longitude"])
                }
            closest_station_data = closest(list_of_stations, start_coordinates)

            # ------------ Fetch Weather Conditions Data -------------------------

            closest_station_url = closest_station_data["id"] + f'/observations?start={{started_at}}&limit=1'.format(
                started_at=serializer_data["start_time"]
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

