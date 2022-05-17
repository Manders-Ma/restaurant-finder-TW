import json
from requests import request
from hunter.connectDB import Restaurant, Location, ParkingLot, Parking, Session
from hunter.config import apiKey_file_path
import requests

with open(apiKey_file_path, "r") as file:
    API_KEY = file.read()

with Session() as s:
    s.execute(
        """
        UPDATE public.restaurant
        SET fk_location_id=public.location.location_id
        FROM public.location
        WHERE public.restaurant."Region"=public.location."Region"
        AND public.restaurant."Town"=public.location."Town";
        """
    )
    s.commit()

status = 1
with Session() as s:
    rests = s.execute(
        """
        SELECT "Name", "Lat", "Lng"
        FROM public.restaurant
        WHERE public.restaurant."Region"='臺北市';
        """
    )



    s.commit()
    for rest in rests:
        print(rest)
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}%2C{}&radius=1000&type=parking&language=zh-TW&key={}".format(
            rest[1],
            rest[2],
            API_KEY
        )
        parkings = dict(json.loads(requests.request("GET", url).text))["results"]
        # print(len(s.query(ParkingLot).filter(ParkingLot.PL_id == parking["place_id"]).all()))
        for parking in parkings:
            if status == 1:
                status = 0
                url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=url&language=zh-TW&key={}".format(
                    parking["place_id"],
                    API_KEY
                )
                info = dict(json.loads(requests.request("GET", url).text))["result"]
                lot = ParkingLot(PL_id=parking["place_id"], PLname=parking["name"], PLurl=info.get("url", ""))
                data = Parking(fk_Name=rest[0], fk_PL_id=parking["place_id"])
                s.add(lot)
                s.add(data)
                s.commit()
            elif len(s.query(ParkingLot).filter(ParkingLot.PL_id == parking["place_id"]).all()) == 0:
                url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=url&language=zh-TW&key={}".format(
                    parking["place_id"],
                    API_KEY
                )
                info = dict(json.loads(requests.request("GET", url).text))["result"]
                lot = ParkingLot(PL_id=parking["place_id"], PLname=parking["name"], PLurl=info.get("url", ""))
                data = Parking(fk_Name=rest[0], fk_PL_id=parking["place_id"])
                s.add(lot)
                s.add(data)
                s.commit()
            else:
                url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=url&language=zh-TW&key={}".format(
                    parking["place_id"],
                    API_KEY
                )
                info = dict(json.loads(requests.request("GET", url).text))["result"]
                data = Parking(fk_Name=rest[0], fk_PL_id=parking["place_id"])
                s.add(data)
                s.commit()