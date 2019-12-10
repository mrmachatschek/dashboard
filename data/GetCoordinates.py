import pandas as pd
import requests

df = pd.read_csv('qol_indices.csv')

cities = df["City"].unique()
URL = "https://api.opencagedata.com/geocode/v1/json"
print(f"\"City\",\"lat\",\"lng\"")

for city in cities:
    PARAMS = {'q':city,
              'key':'<replace>',
              'no_annotations':1
             }
    r = requests.get(url = URL, params = PARAMS)

    data = r.json()
    lat = data["results"][0]["geometry"]["lat"]
    lng = data["results"][0]["geometry"]["lng"]
    print(f"\"{city}\",\"{lat}\",\"{lng}\"")
