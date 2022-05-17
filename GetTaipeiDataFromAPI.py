import pandas as pd
import googlemaps
import requests
import sys
import os
import json
import re
from hunter.config import apiKey_file_path


def getData(type, page_token, API_KEY, dicOfTaipeiRest):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&type={}&pagetoken={}&language=zh-TW&key={}".format(
        "臺北市",
        type,
        page_token,
        API_KEY
    )
    response = dict(json.loads(requests.request("GET", url).text))
    page_token = response.get("next_page_token", "")
    rests = response["results"]
    for rest in rests:
        compound_code = rest["plus_code"]["compound_code"]
        compound_code = re.sub("[a-zA-Z0-9\W]", "", compound_code)
        region = compound_code[-3:]
        town = compound_code[:-3]
        dicOfTaipeiRest["Name"].append(rest["name"])
        dicOfTaipeiRest["Description"].append("")
        dicOfTaipeiRest["Add"].append(rest["formatted_address"])
        dicOfTaipeiRest["Region"].append(region)
        dicOfTaipeiRest["Town"].append(town)

        place_id = rest["place_id"]
        url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=formatted_phone_number%2Curl%2Copening_hours&language=zh-TW&key={}".format(
            place_id,
            API_KEY
        )
        response = dict(json.loads(requests.request("GET", url).text))
        info = response["result"]
        opentime = info.get("opening_hours", "")
        if opentime:
            opentime = opentime["weekday_text"]
            opentime = ",".join(opentime)
        else:
            opentime = ""
        dicOfTaipeiRest["Opentime"].append(opentime)
        dicOfTaipeiRest["Parkinginfo"].append("")
        dicOfTaipeiRest["Tel"].append(info.get("formatted_phone_number", ""))
        dicOfTaipeiRest["url"].append(info.get("url", ""))
    return page_token, dicOfTaipeiRest


with open(apiKey_file_path, "r") as file:
    API_KEY = file.read()

page_token = ""
types = ["restaurant", "bar", "meal_delivery", "meal_takeaway", "cafe"]
dicOfTaipeiRest = {"Name":[], "Description":[], "Add":[], "Region":[], "Town":[],
                    "Opentime":[], "Parkinginfo":[], "Tel":[], "url":[]}
for type in types:
    page_token = ""
    page_token, dicOfTaipeiRest = getData(type, page_token, API_KEY, dicOfTaipeiRest)
    while page_token:
        page_token, dicOfTaipeiRest = getData(type, page_token, API_KEY, dicOfTaipeiRest)

df = pd.DataFrame(data=dicOfTaipeiRest)
df.drop_duplicates(subset=["Name"], ignore_index=True, inplace=True)
df.to_csv("./dataset/TaipeiRest.csv", index=False,
        header=False, encoding="utf-8-sig")