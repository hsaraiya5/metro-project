# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
import json, urllib, http.client
from twilio.twiml.messaging_response import MessagingResponse
from src.utilities.station_utilities import get_station_info, format_return_msg, make_wmata_request
import src.utilities.station_utilities as station_utilities
from src.exceptions.exceptions import WMATAException
import jsonify
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.sql import func


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Station(db.Model):
    station_code = db.Column(db.String(3), primary_key=True)
    station_name = db.Column(db.String(50), nullable=False)
    line_code_1 = db.Column(db.String(2), nullable=False)
    line_code_2 = db.Column(db.String(2), nullable=True)
    line_code_3 = db.Column(db.String(2), nullable=True)
    line_code_4 = db.Column(db.String(2), nullable=True)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip = db.Column(db.String(5), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    def __repr__(self):
        return f'<Station {self.station_name}>'


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