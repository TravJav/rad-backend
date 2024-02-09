import os
from flask import jsonify
from flask_jwt_extended import JWTManager, create_access_token
from radpair.src.health.api.services.helpers.project_util import ProjectUtilHelper


JWT_SECRET = ProjectUtilHelper().get_runtime_env_variable("JWT_SECRET")

jwt = JWTManager()

def init_jwt_auth(app):
    app.config['JWT_SECRET_KEY'] = JWT_SECRET
    jwt.init_app(app)
    return jwt

def generate_jwt_token(uuid: str):
    jwt_secret = JWT_SECRET
    if jwt_secret:
        access_token = create_access_token(identity=uuid)
        return access_token
    else:
        raise RuntimeError("JWT_SECRET is not set!")


@jwt.expired_token_loader
def expired_token_callback(*args):
    return jsonify({
        'message': 'Token has expired',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Invalid token',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({
        'message': 'Missing Authorization Header',
        'error': 'authorization_required'
    }), 401
