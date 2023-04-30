import json
import http, os
from src.exceptions.exceptions import WMATARequestError, InvalidStationName
import urllib

WMATA_HOST_NAME = 'api.wmata.com'


def get_station_info(station_str: str):

    station_str = station_str.lower().replace(" ","")
    with open('./data/station_code_mappings.json', 'r') as f:
        station_data = json.load(f)

    station_code, station_name = None, None
    for station in station_data['stations']:
        for key, value in station.items():
            if key=='Name' and (station_str in value.lower().replace(" ","")):
                station_code = station['Code']
                station_name = station['Name']
    if station_code is None:
        raise InvalidStationName("Station Name is invalid")
    else:
        return station_code, station_name



def format_return_msg(station_name: str, station_predictions: dict()):

    return_str = f"Trains at {station_name} station:"
    if len(station_predictions) != 0:
        for trains in station_predictions['Trains']:
            return_str+=f"\n\n{trains['Line']} line train headed towards {trains['Destination']}"
            if trains['Min'] == 'ARR' or trains['Min'] == 'BRD':
                return_str+=f". The train is {trains['Min']}."
            else: 
                return_str+=f" arriving in {trains['Min']} min."
    return return_str


def make_wmata_request(verb: str, path: str):

    headers = {
        'api_key': os.getenv('METRO_API_KEY')
    }
    try:
        conn = http.client.HTTPSConnection(WMATA_HOST_NAME)
        conn.request(verb, path, "{body}", headers)
        response = conn.getresponse()
    except WMATARequestError as e:
        print("WMATA request failed.")
        return "Failed"

    data = response.read()
    json_response = json.loads(data)
    conn.close()
    
    return json_response

def update_station_mapping():
    lines = ['YL', 'RD', 'SV', 'GR', 'BL', 'OR']
    mappings = {
        "stations": []
    }
    for line in lines:
        params = urllib.parse.urlencode({
            'LineCode': line
        })

        line_data = make_wmata_request("GET", "/Rail.svc/json/jStations?%s" % params)         

        for station in line_data["Stations"]:
            mappings["stations"].append(station)

    output = json.dumps(mappings, indent = 2)
    with open("./data/station_code_mappings.json", "w") as outfile:
        outfile.write(output)
    return