from src.main import db, Station,app
import json

with app.app_context():

    db.drop_all()
    db.create_all()

    with open('./data/station_code_mappings.json', 'r') as f:
            station_data = json.load(f)

    for station in station_data['stations']:
        if len(Station.query.filter_by(station_code=station['Code']).all()) == 0:
            station_entry = Station(station_code=station['Code'], \
                                    station_name=station['Name'], \
                                    line_code_1=station['LineCode1'], \
                                    line_code_2=station['LineCode2'], \
                                    line_code_3=station['LineCode3'], \
                                    line_code_4=station['LineCode4'], \
                                    latitude=station['Lat'], \
                                    longitude=station['Lon'], \
                                    street=station['Address']['Street'], \
                                    city=station['Address']['City'], \
                                    state=station['Address']['State'], \
                                    zip=station['Address']['Zip'])
            db.session.add(station_entry)
            db.session.commit()




    print(Station.query.all())