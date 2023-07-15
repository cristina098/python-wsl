import pandas as pd
import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=47.151726&lon=27.587914&altitude=60"
req = requests.get(url, headers=headers)

meteo = json.loads(req.text)
print(meteo)

