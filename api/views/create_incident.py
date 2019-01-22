from flask import Blueprint, jsonify, json, request

from api.helpers.auth_token import (
    token_required,
    non_admin,
    get_current_identity,
)

create_incident_bp = Blueprint(
    "new_incident", __name__, url_prefix="/api/v2"
)
from api.models.incident import Incident
from api.helpers.validation import validate_new_incident

incident_obj = Incident()


@create_incident_bp.route("/red-flags", methods=["POST"])
@token_required
@non_admin
def new_red_flag():
    if not request.data:
        return (
            jsonify(
                {
                    "error": "Please provide red-flag Data",
                    "status": 400,
                }
            ),
            400,
        )
    data = request.get_json(force=True)

    new_incident_data = {
        "title": data.get("title"),
        "location": data.get("location"),
        "comment": data.get("comment"),
        "images": data.get("Images"),
        "videos": data.get("Videos"),
    }

    not_valid = validate_new_incident(**new_incident_data)
    response = None

    if not_valid:
        response = not_valid
    elif not incident_obj.incident_record_exists(
            new_incident_data["title"], new_incident_data["comment"]
    ):

        new_incident_data["user_id"] = get_current_identity()
        new_incident_data["inc_type"] = 'red-flag'

        new_db_incident_details = incident_obj.insert_incident(
            **new_incident_data
        )

        response = (
            jsonify(
                {
                    "status": 201,
                    "data": [
                        {
                            "red-flag": new_db_incident_details,
                            "message": "Created red-flag record",
                        }
                    ],
                }
            ),
            201,
        )
    else:

        response = (
            jsonify(
                {
                    "status": 409,
                    "error": "red-flag record already exists",
                }
            ),
            409,
        )

    return response
