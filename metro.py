import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import yaml
import sys


with open("wmataApiKeys.yaml", "r") as stream:
    try:
        keys = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

f = open('station_code_mappings.json')
station_code_mappings = json.load(f)


headers = {
    'api_key': keys['apiKey']
}

line = input("Enter the line you are on: ")
station_name = input("Enter the station you are at: ").lower()

for station in station_code_mappings[line]['Stations']:
    for key, value in station.items():
        if key=='Name':
            if station_name in value.lower():
                code = station['Code']

try:
    conn = http.client.HTTPSConnection('api.wmata.com')
    conn.request("GET", f"/StationPrediction.svc/json/GetPrediction/{code}", "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    station_predictions = json.loads(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))


for trains in station_predictions['Trains']:
    if trains['Min'] == 'ARR' or trains['Min'] == 'BRD':
        print(f"{trains['Line']} line train headed towards {trains['Destination']}. The train is {trains['Min']}.")
    else:
        print(f"{trains['Line']} line headed towards {trains['Destination']} arriving in {trains['Min']} min.")
