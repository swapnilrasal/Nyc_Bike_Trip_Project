import csv
import os
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from Nyc_Bike_Trip.models import BikeTrip
# import requests
from zipfile import ZipFile
import wget

# from reports.models import UNOOfficeReport, ACLandOfficeReport


class Command(BaseCommand):
    help = "Insert Bike Trip Data from a CSV file. " \
           "Zip file name(s) should be passed. " \

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = BikeTrip

    def insert_bike_trip_data_to_db(self, objs):
        try:
            self.stdout.write(self.style.SUCCESS('Inserting Data into BikeTrip Table'))
            msg = self.model_name.objects.bulk_create(objs)

        except Exception as e:
            raise CommandError("Error in inserting {}: {}".format(
                self.model_name, str(e)))

    def download_zip_file(self, filename):
        url = "https://s3.amazonaws.com/tripdata/"
        file_path = os.path.join(url, filename)
        current_path = os.path.dirname(os.path.abspath(__file__)).split('/')[-1]

        req = wget.download(file_path,out =current_path)
        # # Split file_path to get the file name
        zip_filename = file_path.split('/')[-1]
        csv_filename = zip_filename.replace(".zip",".csv")
        zip_file_path = current_path+f'\{{fname}}'.format(fname=zip_filename)
        print(zip_file_path)

        self.stdout.write(self.style.SUCCESS('Extracting:{}'.format(filename)))
        with ZipFile(zip_file_path, 'r') as zipObj:
        # Get a list of all archived file names from the zip
            listOfFileNames = zipObj.namelist()
            # print(listOfFileNames)
            # Iterate over the file names
            for f_name in listOfFileNames:
                # Check filename endswith csv
                if f_name == csv_filename:
                    # Extract a single file from zip
                    zipObj.extract(f_name, current_path)

        if os.path.exists(zip_file_path):
            self.stdout.write(self.style.SUCCESS('Deleting:{}'.format(filename)))
            os.remove(zip_file_path)

        return current_path+f'\{{fname}}'.format(fname=csv_filename)

    def add_arguments(self, parser):
        parser.add_argument('filenames',
                            nargs='+',
                            type=str,
                            help="Inserts Bike Trip Data from ZIP file")

    def handle(self, *args, **options):

        for filename in options['filenames']:
            self.stdout.write(self.style.SUCCESS('Downloading:{}'.format(filename)))
            file_path = self.download_zip_file(filename)

            try:
                with open(file_path) as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    list_of_dict = list(csv_reader)
                    objs = [
                        BikeTrip(
                            tripduration=row['tripduration'],
                            starttime=row['starttime'],
                            stoptime=row['stoptime'],                            
                        )
                        for row in list_of_dict
                    ]
                    self.insert_bike_trip_data_to_db(objs)

                if os.path.exists(file_path):
                    self.stdout.write(self.style.SUCCESS('Deleting:{}'.format(file_path)))
                    os.remove(file_path)
        
                self.stdout.write(self.style.SUCCESS('Data Inserted Successfully'))

            except FileNotFoundError:
                raise CommandError("File {} does not exist".format(
                    file_path))