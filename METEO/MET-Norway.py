import requests
import json
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

url = "https://www.meteoromania.ro/wp-json/meteoapi/v2/starea-vremii"
req = requests.get(url, headers=headers)
stareaVremii = json.loads(req.text)
stareaVremiiLocations = stareaVremii['features']

myDict = {}

print(f"Read {len(stareaVremiiLocations)} locations from Meteo Romania at {stareaVremii['date']}")
for i in range(len(stareaVremiiLocations)):
    if (stareaVremiiLocations[i]['properties']['nume'] == "IASI"):
        currentTime = datetime.datetime.fromisoformat(stareaVremii['date']) + datetime.timedelta(hours=1)
        currentTime = currentTime.replace(tzinfo=None)
        print(f"[{i}] {stareaVremiiLocations[i]['properties']['nume']}, {currentTime.year}.{currentTime.month}.{currentTime.day} / {currentTime.hour}:00   --> {stareaVremiiLocations[i]['properties']['tempe']}")
        myDict["RO"] = {"now": f"{currentTime.isoformat()}", "temp": float(stareaVremiiLocations[i]['properties']['tempe'])}
        break


url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=47.151726&lon=27.587914&altitude=60"
req = requests.get(url, headers=headers)
metNorway = json.loads(req.text)
metNorwayTimeseries = metNorway['properties']['timeseries']



print(f"Read {len(metNorwayTimeseries)} from MET Norway")

myDict["METNO"] = []

for i in range(len(metNorwayTimeseries)):
    prognosisTime = datetime.datetime.strptime(metNorwayTimeseries[i]['time'], '%Y-%m-%dT%H:%M:%SZ')
    prognosisTime += datetime.timedelta(hours=3)
    if (prognosisTime.hour in [3, 9, 15, 21]):
        #print(f"{prognosisTime} --> {metNorwayTimeseries[i]['data']['instant']['details']['air_temperature']}")
        myDict["METNO"].append({"now": f"{prognosisTime.isoformat()}", "temp": metNorwayTimeseries[i]['data']['instant']['details']['air_temperature']})

filename = f"MET-Norway-{myDict['RO']['now']}.json"
print(f"Saving {filename}")

with open(filename, "w") as outfile:
    outfile.write(json.dumps(myDict, indent=4))
