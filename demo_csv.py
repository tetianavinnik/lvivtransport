
import json
from google.transit import gtfs_realtime_pb2
import requests
from google.protobuf.json_format import MessageToDict
import schedule
import time
import sys
import gtfs_kit as gk
from gtfslite.gtfs import GTFS
import csv
from google.protobuf.json_format import MessageToJson
from google.protobuf.descriptor import FieldDescriptor


n=0
def func():
    global n
    n+=1
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('http://track.ua-gis.com/gtfs/lviv/vehicle_position')
    feed.ParseFromString(response.content)
    f = feed.entity
    
    with open(r"C:\Users\TETYANA\Desktop\Транспорт\data_4h.csv", 'a', newline='') as file:
        if n==1:
            file.write("id,trip_id,route_id,schedule_relationship,vehicle_id,license_plate,latitude,longitude,bearing,odometer,speed,timestamp,congestion_level\n")


        for marshrutka in f:
            lst = [marshrutka.id, marshrutka.vehicle.trip.trip_id, marshrutka.vehicle.trip.route_id, str(marshrutka.vehicle.trip.schedule_relationship),
                   marshrutka.vehicle.vehicle.id, marshrutka.vehicle.vehicle.license_plate, str(marshrutka.vehicle.position.latitude), str(marshrutka.vehicle.position.longitude),
                   str(marshrutka.vehicle.position.bearing), str(marshrutka.vehicle.position.odometer), str(marshrutka.vehicle.position.speed), str(marshrutka.vehicle.timestamp), str(marshrutka.vehicle.congestion_level)]
            file.write(",".join(lst)+"\n")

    if n==1440:
        sys.exit()


schedule.every(10).seconds.do(func)
while True:
    schedule.run_pending()
    time.sleep(0.083)
