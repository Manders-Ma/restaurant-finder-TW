import json
import pandas as pd
import urllib.request as req

from requests import head

url = "https://gis.taiwan.net.tw/XMLReleaseALL_public/restaurant_C_f.json"

with req.urlopen(url) as response:
    data = json.load(response)
    rests = data["XML_Head"]["Infos"]["Info"]
    del data

dicOfRest = {"Name": [], "Description": [], "Add": [], "Region": [],
             "Town": [], "Opentime": [], "Parkinginfo": [], "Tel": [], "url": []}

for rest in rests:
    dicOfRest["Name"].append(rest["Name"])
    dicOfRest["Description"].append(rest["Description"])
    dicOfRest["Add"].append(rest["Add"])
    dicOfRest["Region"].append(rest["Region"])
    dicOfRest["Town"].append(rest["Town"])
    dicOfRest["Opentime"].append(rest["Opentime"])
    dicOfRest["Parkinginfo"].append(rest["Parkinginfo"])
    dicOfRest["Tel"].append(rest["Tel"])
    dicOfRest["url"].append("")

df = pd.DataFrame(data=dicOfRest)
df.dropna(subset=["Region", "Town", "Add"], inplace=True)
df.drop_duplicates(subset=["Name"], ignore_index=True, inplace=True)
df.to_csv("./dataset/restaurant.csv", index=False,
          header=False, encoding="utf-8-sig")
