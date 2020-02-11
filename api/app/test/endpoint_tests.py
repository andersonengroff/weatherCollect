import pytest
import requests
import json


def test_server_status_code_ok():
    response = requests.get('http://localhost:5000')
    assert response.status_code == 200
