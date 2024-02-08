
import logging
from flask import Blueprint, jsonify, request
authentication_bp = Blueprint("authentication", __name__)

@authentication_bp.route('/login', methods=['POST'])
def login() -> jsonify:
    try:
        data = request.get_json()
        password = data.get('password')
        email = data.get('email')
        if email and password:
            return jsonify(
            {
                "success": True,
                "message": "Welcome",
            }
        )
    except (KeyError, ValueError) as e:
        logging.exception("Issue parsing response object: {} ".format(e))
        return jsonify(
            {
                "success": False,
                "message": "Something went wrong, please try again",
            }
        )
