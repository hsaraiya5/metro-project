# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
import json, urllib, http.client
from twilio.twiml.messaging_response import MessagingResponse
from src.utilities.station_utilities import get_station_info, format_return_msg, make_wmata_request
import src.utilities.station_utilities as station_utilities
from src.exceptions.exceptions import WMATAException
import jsonify

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def listen():

    station_name = request.values.get('Body', None)
    station_code, station_name = get_station_info(station_name)
   
    station_predictions = make_wmata_request("GET", f"/StationPrediction.svc/json/GetPrediction/{station_code}")
   
    resp = MessagingResponse()
    resp.message(format_return_msg(station_name, station_predictions))

    return str(resp)
 

@app.route('/station-mappings')
def update_station_mapping(): 
    
    station_utilities.update_station_mapping()
    return("Mappings updated successfully")

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()