from flask import json

from api.helpers.responses import supported_end_points

def test_invalid_url(client):
    response = client.delete("api/v1/")
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["supportedEndPoints"] == supported_end_points
    assert data["error"] == "Endpoint for specified URL does not exist"

def test_method_not_allowed(client):
    response = client.delete("/")
    assert response.status_code == 405
    data = json.loads(response.data.decode())
    assert data["error"] == "Method not allowed"
    assert data["supportedMethods"] == supported_end_points

def test_welcome_message(client):
    response = client.get("/")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["message"] == "Welcome to iReporter API V1"
    assert data["status"] == 200

def test_bad_formar_json_data(client):
    mimetype = "application/json"
    response = client.post(
        "/api/v1/auth/login",
        data="admin Password123",headers = {"Content-Type": mimetype, "Accept": mimetype}
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["error"] == "Bad JSON format data"
    assert data["status"] == 400
