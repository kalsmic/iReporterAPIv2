from flask import json

from api.helpers.responses import invalid_token_message, expired_token_message
from .base import user2_header, expired_token_header


# GET ALL RED-FLAG RECORDS


def test_get_all_red_flags_without_token(client):
    # test only logged in user get red flags
    response = client.get("api/v1/red-flags")
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {"error": invalid_token_message, "status": 401}


def test_get_all_red_flags_with_expired_token(client):
    # test only logged in user get red flags
    response = client.get("api/v1/red-flags", headers=expired_token_header)
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data == {"error": expired_token_message, "status": 401}


def test_get_all_red_flags(client):
    response = client.get("api/v1/red-flags", headers=user2_header)
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["data"][0]["createdBy"] == 3


# GET A SPECIFIC RED-FLAG RECORD
def test_get_a_red_flag_which_does_not_exist(client):
    response = client.get("api/v1/red-flags/12", headers=user2_header)
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data["error"] == "Red-flag record does not exist"


def test_get_a_red_flag(client):
    response = client.get("api/v1/red-flags/1", headers=user2_header)
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["status"] == 200
    assert data["data"][0][0]["Images"] == ["image3.jpg", "image4.jpg"]


def test_get_a_red_flag_with_invalid_id(client):
    response = client.get("api/v1/red-flags/fs", headers=user2_header)
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data["status"] == 400
    assert data["error"] == "Red-flag id must be an integer"
