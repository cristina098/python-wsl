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
        currentTime = datetime.datetime.fromisoformat(stareaVremii['date'])
        currentTime = currentTime.replace(tzinfo=None)
        print(f"[{i}] {stareaVremiiLocations[i]['properties']['nume']}, {currentTime.year}.{currentTime.month}.{currentTime.day} / {currentTime.hour}:00   --> {stareaVremiiLocations[i]['properties']['tempe']}")
        myDict["RO"] = {"now": f"{currentTime.isoformat()}", "temp": float(stareaVremiiLocations[i]['properties']['tempe'])}
        break

#############################################################

url = "https://api.open-meteo.com/v1/forecast?latitude=47.151726&longitude=27.587914&hourly=temperature_2m&timezone=Africa%2FCairo"
req = requests.get(url, headers=headers)
OpenMeteo = json.loads(req.text)
OpenMeteoTimes = OpenMeteo['hourly']['time']
OpenMeteoTemps = OpenMeteo['hourly']['temperature_2m']


print(f"Read {len(OpenMeteoTimes)} from OpenMeteo")

myDict["OPENMETEO"] = []

for i in range(len(OpenMeteoTimes)):
    prognosisTime = datetime.datetime.strptime(OpenMeteoTimes[i], '%Y-%m-%dT%H:%M')
    deltaTime = prognosisTime - currentTime
    if (prognosisTime.hour in [3, 9, 15, 21]) and (deltaTime.total_seconds() > -2000):
        #print(f"{prognosisTime} --> {OpenMeteoTemps[i]}")
        myDict["OPENMETEO"].append({"now": f"{prognosisTime.isoformat()}", "temp": OpenMeteoTemps[i]})

filename = f"Open-Meteo-{myDict['RO']['now']}.json"
print(f"Saving {filename}")

with open(filename, "w") as outfile:
    outfile.write(json.dumps(myDict, indent=4))
