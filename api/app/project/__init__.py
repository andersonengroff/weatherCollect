import requests
import json
import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy



def create_app():
    app = Flask(__name__)
    app.config.from_object("project.config.Config")

    return app


app = create_app()
db = SQLAlchemy(app)

# get Model
from project.model import Collector, time_transform, fact_transform, fact_clean

@app.route("/")
def hello_world():
    return jsonify(service="works fine!")

@app.route('/weather/collect/<int:station_id>', methods=['POST'])
def handle_collect_weather(station_id):
    if request.method == 'POST':
        url = f'https://openweathermap.org/data/2.5/weather/?appid=b6907d289e10d714a6e88b30761fae22&units=metric&id={station_id}'
        response = requests.get(url)
        json_data = json.loads(response.text)
        rain = 0
        if "rain" in json_data:
            rain = json_data['rain']['1h']

        if json_data['cod'] == 200:
            db.session.add(
                Collector(
                    id_station = json_data['id'],
                    datetime = datetime.datetime.fromtimestamp(json_data['dt']), 
                    rain = rain,
                    max_temperature = json_data['main']['temp_max'],
                    origin = 'W'
                )
            )
            db.session.commit()
            
            return jsonify(message="success")

        return jsonify(message="Invalid station_id"), 400


@app.route('/forecast/collect/<int:station_id>', methods=['POST'])
def handle_collect_forecast(station_id):
    if request.method == 'POST':
        url = f'https://openweathermap.org/data/2.5/forecast/daily/?appid=b6907d289e10d714a6e88b30761fae22&units=metric&id={station_id}'
        response = requests.get(url)
        json_data = json.loads(response.text)

        if json_data['cod'] == "200":
            for item in json_data['list']:
                rain = 0
                if "rain" in item:
                    rain = item['rain']
                db.session.add(
                    Collector(
                        id_station = json_data['city']['id'],
                        datetime = datetime.datetime.fromtimestamp(item['dt']), 
                        rain = rain,
                        max_temperature = item['temp']['max'],
                        origin = 'F'
                    )
                )
            db.session.commit()

            return jsonify(message="success")

        return jsonify(message="Invalid station_id"), 400
    
@app.route('/transformation/fact', methods=['POST'])
def handle_transformation_fact():
    if request.method == 'POST':
        try:
            fact_clean()
            time_transform()
            fact_transform()
        except:
            return jsonify(message="Transformation Failed"), 500


    return jsonify(message="success")
    
