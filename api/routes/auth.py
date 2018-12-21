from flask import (
    Blueprint, jsonify, request, json
)

from api.helpers import request_data_required
from api.models.user import (
    User,
    check_if_user_exists,
    sign_up_user,
    is_valid_credentials
)

users_bp = Blueprint('users_bp', __name__, url_prefix='/api/v1')


@users_bp.route('/auth/register', methods=['POST'])
@request_data_required
def register():
    """Expects Parameters:
        firstname: String
        lastname: String
        othernames: String
        username: String
        email: String
        phoneNumber:string
        password:string
    """

    new_user = json.loads(request.data)
    try:
        firstname = new_user['firstname']
        lastname = new_user['lastname']
        othernames = new_user['othernames']
        username = new_user['username']
        email = new_user['email']
        phoneNumber = new_user['phoneNumber']
        password = new_user['password']

    except KeyError:
        return jsonify({
            'error': "Please provide the correct keys for the data",
            "status": 400
        }), 400

    new_user = User(
        firstname=firstname,
        lastname=lastname,
        othernames=othernames,
        username=username,
        email=email,
        password=password,
        phoneNumber=phoneNumber
    )

    error = new_user.validate_input_data()
    if error:
        return jsonify({"error": error, "status": 400}), 400

    user_exists = check_if_user_exists(new_user)
    if user_exists:
        return jsonify({"error": user_exists, "status": 403}), 403

    # Register new user
    sign_up_user(new_user)
    return jsonify({
        "status": 201,
        "data": new_user.get_user_details()
    }), 201


@users_bp.route("/auth/login", methods=['POST'])
@request_data_required
def login():
    """Expects Parameters:
        username: String
        password:string
    """

    user_credentials = json.loads(request.data)
    try:
        username = user_credentials['username']
        password = user_credentials['password']

        # submit credentials
        data = is_valid_credentials(username, password)
        if data:
            return jsonify({
                "token": data,
                "status": 200,
                "message": "Logged in successfully"
            }), 200
        return jsonify({
            'error': "Invalid credentials",
            "status": 401
        }), 401

    except KeyError:
        return jsonify({
            'error': "Please provide the correct keys for the data",
            "status": 400
        }), 400
