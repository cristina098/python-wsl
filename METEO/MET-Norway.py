import pandas as pd
import requests
import json
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

url = "https://www.meteoromania.ro/wp-json/meteoapi/v2/starea-vremii"
req = requests.get(url, headers=headers)
stareaVremii = json.loads(req.text)
stareaVremiiLocations = stareaVremii['features']

print(f"Read {len(stareaVremiiLocations)} locations from Meteo Romania at {stareaVremii['date']}")
for i in range(len(stareaVremiiLocations)):
    if (stareaVremiiLocations[i]['properties']['nume'] == "IASI"):
        currentTime = datetime.datetime.fromisoformat(stareaVremii['date'])
        print(f"[{i}] {stareaVremiiLocations[i]['properties']['nume']}, {currentTime.year}.{currentTime.month}.{currentTime.day} / {currentTime.hour}:00   --> {stareaVremiiLocations[i]['properties']['tempe']}")
        break


url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=47.151726&lon=27.587914&altitude=60"
req = requests.get(url, headers=headers)
metNorway = json.loads(req.text)
metNorwayTimeseries = metNorway['properties']['timeseries']



print(f"Read {len(metNorwayTimeseries)} from MET Norway")

#for i in range(len(metNorwayTimeseries)):
#    currentTime = datetime.datetime.strptime(metNorwayTimeseries[i]['time'], '%Y-%m-%dT%H:%M:%SZ')
#    print(f"{currentTime} --> {metNorwayTimeseries[i]['data']['instant']['details']['air_temperature']}")




