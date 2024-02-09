
import logging
from flask import Blueprint, jsonify, request
authentication_bp = Blueprint("authentication", __name__)

@authentication_bp.route('/login', methods=['POST'])
def login() -> jsonify:
    """
    login that should in the real world radpair MVP backend.. 
    go to the services/queries and create a DB session object connect to the db
    and then make sure the hash matches the input password
    Returns:
        jsonify: login status
    """
    try:
        data: str = request.get_json()
        password: str = data.get('password')
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
