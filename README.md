# Nyc_Bike_Trip_Project
Nyc_Bike_Trip_Project

*************************************************************************
# requirements
*************************************************************************
python version - Python 3.8.2 or greater
pip version - pip 20.1.1
*************************************************************************

# Steps to Setup this project

# create virtual environment
*************************************************************************
> virtualenv BikeTrip
> BikeTrip\Scripts\activate
*************************************************************************

# After this install requirements
*************************************************************************
> cd .\Nyc_Bike_Trip_Project\
> pip install -r .\requirements\requirements.txt
> cd .\Nyc_Bike_Trip_Project
*************************************************************************

# Then Run Following for Migrations
*************************************************************************
> python manage.py makemigrations
> python manage.py migrate
*************************************************************************

# Then create Super User to Access Admin Panel
*************************************************************************
> python manage.py createsuperuser
*************************************************************************

# To insert Data from zip csv file using management command

** before excuting this command check you are correct folder or not
** go to Nyc_Bike_Trip_Project this folder first
** make sure you have activated your virtualenv

*************************************************************************
> python manage.py insert_bike_trip_records filename
*************************************************************************

# example -
*************************************************************************
> python manage.py insert_bike_trip_records JC-202112-citibike-tripdata.csv.zip

** note please use files which was created after feb 2021 - new format is applied after this date.

*************************************************************************

# After Succesfully Excuting this Data is inserted into Your Database Run Server
*************************************************************************
> python manage.py runserver
*************************************************************************

# For checking APIS you can Use POSTMAN or swagger also

*************************************************************************
Swagger Endpoint - http://127.0.0.1:8000/
*************************************************************************