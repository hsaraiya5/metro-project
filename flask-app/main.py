# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
import json, urllib, http.client
import yaml
 
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
 

with open("../wmataApiKeys.yaml", "r") as stream:
    try:
        keys = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

headers = {
        'api_key': keys['apiKey']
}



# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'
 

@app.route('/station-trains/<line_name>/<name>')
def get_upcoming_trains(line_name, name):
    f = open('station_code_mappings.json')
    station_code_mappings = json.load(f)


    headers = {
        'api_key': keys['apiKey']
    }

    line = line_name
    station_name = name

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

    return_str = ""
    for trains in station_predictions['Trains']:
        if trains['Min'] == 'ARR' or trains['Min'] == 'BRD':
            return_str+="\n"
            return_str+=f"{trains['Line']} line train headed towards {trains['Destination']}. The train is {trains['Min']}."
        else:
            return_str+="\n"
            return_str+=f"{trains['Line']} line headed towards {trains['Destination']} arriving in {trains['Min']} min."
    return return_str

@app.route('/station-mappings')
def update_station_mapping():

    with open("../wmataApiKeys.yaml", "r") as stream:
        try:
            keys = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    
    lines = ['YL', 'RD', 'SV', 'GR', 'BL', 'OR']
    mappings = {}
    for line in lines:
        params = urllib.parse.urlencode({
            'LineCode': line
        })

        try:
            conn = http.client.HTTPSConnection('api.wmata.com')
            conn.request("GET", "/Rail.svc/json/jStations?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            line_data = json.loads(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
        mappings[line] = line_data

    output = json.dumps(mappings, indent = 2)
    with open("station_code_mappings.json", "w") as outfile:
        outfile.write(output)
    
    return(mappings)

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()