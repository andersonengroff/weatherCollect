import pytest
import requests
import json


def test_server_status_code_ok():
    response = requests.get('http://localhost:5000')
    assert response.status_code == 200

def test_weather_collect_ok():
    response = requests.post('http://localhost:5000/weather/collect/2640729')
    json_data = json.loads(response.text)
    assert json_data['message'] == 'success'

def test_weather_collect_wrong_city():
    response = requests.post('http://localhost:5000/weather/collect/999111')
    json_data = json.loads(response.text)
    assert json_data['message'] == 'Invalid station_id' and response.status_code == 400

def test_forecast_collect_ok():
    response = requests.post('http://localhost:5000/forecast/collect/2640729')
    json_data = json.loads(response.text)
    assert json_data['message'] == 'success'

def test_forecast_collect_wrong_city():
    response = requests.post('http://localhost:5000/forecast/collect/999111')
    json_data = json.loads(response.text)
    assert json_data['message'] == 'Invalid station_id' and response.status_code == 400