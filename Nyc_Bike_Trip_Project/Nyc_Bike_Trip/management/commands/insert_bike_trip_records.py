import os
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from Nyc_Bike_Trip.models import BikeTrip
import wget
import pandas as pd
import zipfile


class Command(BaseCommand):
    help = "Insert Bike Trip Data from a CSV file. " \
           "Zip file name(s) should be passed. " \

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = BikeTrip

    def insert_bike_trip_data_to_db(self, objs):
        try:
            self.stdout.write(self.style.SUCCESS('Inserting Data into BikeTrip Table'))
            self.model_name.objects.all().delete()
            msg = self.model_name.objects.bulk_create(objs)

        except Exception as e:
            raise CommandError("Error in inserting {}: {}".format(
                self.model_name, str(e)))

    def download_zip_file(self, filename):
        # import pdb
        # pdb.set_trace()
        url = "https://s3.amazonaws.com/tripdata/"
        file_path = os.path.join(url, filename)
        current_path = os.path.dirname(os.path.abspath(__file__)).split('/')[-1]
        print("\n")
        # req = wget.download(file_path, out=current_path)
        # # Split file_path to get the file name
        zip_filename = file_path.split('/')[-1]

        zip_file_path = current_path+f'\{{fname}}'.format(fname=zip_filename)
        print("\n")
        self.stdout.write(self.style.SUCCESS('Extracting:{}'.format(filename)))
        print("\n")
        self.stdout.write(self.style.SUCCESS('Fetching Data From Zip File :{}'.format(filename)))
        zf = zipfile.ZipFile(zip_file_path) 
        df = pd.read_csv(zf.open(zipfile.ZipFile.namelist(zf)[0]))
        total_rows = df.shape[0]
        print("\n")
        self.stdout.write(self.style.SUCCESS('Total Records :{}'.format(total_rows)))
        print("\n") 
        resp = {}
        resp["df"] = df
        resp["zip_file_path"] = zip_file_path

        # print(df)
        return resp

    def add_arguments(self, parser):
        parser.add_argument('filenames',
                            nargs='+',
                            type=str,
                            help="Inserts Bike Trip Data from ZIP file")

    def handle(self, *args, **options):

        for filename in options['filenames']:
            print("*********************************************************************************************")
            self.stdout.write(self.style.SUCCESS('Downloading:{}'.format(filename)))
            resp = self.download_zip_file(filename)
            # import pdb
            # pdb.set_trace()
            resp["df"].iloc[:, 2] = pd.to_datetime(resp["df"].iloc[:, 2])
            resp["df"].iloc[:, 3] = pd.to_datetime(resp["df"].iloc[:, 3])
            try:
                from dateutil import parser
                from django.utils import timezone

                objs = [
                    BikeTrip(
                        bikeid=(row[0] if not pd.isnull(row[0]) else None),
                        rideable_type=(row[1] if not pd.isnull(row[1]) else None),
                        started_at=(timezone.make_aware(row[2], timezone.get_current_timezone()) if not pd.isnull(row[2]) else None),
                        ended_at=(timezone.make_aware(row[3], timezone.get_current_timezone()) if not pd.isnull(row[3]) else None),
                        start_station_id=(row[4] if not pd.isnull(row[4]) else None),
                        start_station_name=(row[5] if not pd.isnull(row[5]) else None),
                        end_station_id=(row[6] if not pd.isnull(row[6]) else None),
                        end_station_name=(row[7] if not pd.isnull(row[7]) else None),
                        start_lat=(row[8] if not pd.isnull(row[8]) else None),
                        start_lon=(row[9] if not pd.isnull(row[9]) else None),
                        end_lat=(row[10] if not pd.isnull(row[10]) else None),
                        end_lon=(row[11] if not pd.isnull(row[11]) else None),
                        member_casual=(row[12] if not pd.isnull(row[12]) else None),
                    )
                    for index, row in resp["df"].iterrows()
                ]
                self.insert_bike_trip_data_to_db(objs)

                if os.path.exists(resp["zip_file_path"]):
                    print("\n")
                    self.stdout.write(self.style.SUCCESS('Deleting:{}'.format(resp["zip_file_path"])))
                    os.remove(resp["zip_file_path"])

                print("\n")
                self.stdout.write(self.style.SUCCESS('Data Inserted Successfully'))
                print("\n*********************************************************************************************")
            except FileNotFoundError:
                raise CommandError("File {} does not exist")