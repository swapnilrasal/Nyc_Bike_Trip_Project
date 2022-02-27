from django.urls import path
from Nyc_Bike_Trip import views

urlpatterns = [
    path('get_bike_trip_list/', views.BikeTripListAPIView.as_view(),
         name='get_bike_trip_list/'),
    path('get_single_trip_instance/<str:bikeid>', views.GetSingleTripInstanceView.as_view(),
         name='get_single_trip_instance/')
]
