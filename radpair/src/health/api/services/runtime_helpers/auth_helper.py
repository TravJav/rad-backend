from typing import Type

from flask import Request
from flask_jwt_extended import get_jwt_identity
from werkzeug.local import LocalProxy


def extract_client_request_data(request: Type[Request]) -> dict:
    """
    called on every protected route in the blueprints
    this function takes the decoded payload of the jwt if authenticated
    and the proceeds to extract the values of the returned type of
    werkzeug.local.LocalProxy class
    Args:
        request (Type[Request]): _description_

    Returns:
        dict: _description_
    """
    client_info: LocalProxy = extract_jwt_data_from_token()
    return {
        "username": request.headers["username"],
    }


def extract_jwt_data_from_token():
    """
    helper method to extract the jwt and it's required values to build the
    return object with the key values for down stream proccesing of the requests

    Returns:
        class werkzeug.local.LocalProxy : class representation of decoded token
        and it's payload values
    """
    return get_jwt_identity
