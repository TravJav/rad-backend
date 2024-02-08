
import bcrypt

from radpair.src.health.api.extensions.jwt_configuration import generate_jwt_token


class AuthenticationHandler:

    def compare_password(self, comparison_password, hashed_pass):
        comparison_password = comparison_password.encode('utf-8')
        hashed_pass = hashed_pass.encode('utf-8')
        auth_flag = bcrypt.checkpw(comparison_password, hashed_pass)
        if auth_flag:
            return True
        else:
            return False
    
    def generate_jwt_session_token(self, uuid:str):
        return generate_jwt_token(uuid)
