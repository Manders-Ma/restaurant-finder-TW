import re
import googlemaps
from hunter.connectDB import Session, Restaurant, Location
from hunter.config import apiKey_file_path


def getRegionTown(add):
    updAdd = re.sub("[A-Za-z0-9]", "", add)
    region = updAdd[0:3]
    if "區" in updAdd[3:]:
        endIndex = updAdd[3:].index("區") + 3
        town = updAdd[3:endIndex + 1]
    elif "鄉" in updAdd[3:]:
        endIndex = updAdd[3:].index("鄉") + 3
        town = updAdd[3:endIndex + 1]
    elif "鎮" in updAdd[3:]:
        endIndex = updAdd[3:].index("鎮") + 3
        town = updAdd[3:endIndex + 1]
    else:
        endIndex = updAdd[3:].index("市") + 3
        town = updAdd[3:endIndex + 1]

    return region, town


def calc_distance(location_id, time_threshold, origin, mode, mode_para):
    with open(apiKey_file_path, "r") as file:
        API_KEY = file.read()
    map_client = googlemaps.Client(key=API_KEY)
    s = Session()
    rests = s.query(Restaurant).filter(
        Restaurant.fk_location_id == location_id).all()
    output = []
    for rest in rests:
        destination = rest.Add
        if mode_para:
            response = map_client.distance_matrix(
                origins=origin, destinations=destination, mode=mode, transit_mode=mode_para)
        else:
            response = map_client.distance_matrix(
                origins=origin, destinations=destination, mode=mode)

        traffic_time = round(
            response["rows"][0]["elements"][0]['duration']['value'] / 60)
        if traffic_time <= time_threshold:
            output.append((traffic_time, rest))

    output = sorted(output, key=lambda x: x[0])
    s.close()
    return output
