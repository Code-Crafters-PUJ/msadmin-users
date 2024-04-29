import jwt
from jwt.exceptions import InvalidTokenError
from config.settings import SECRET_KEY



class JWTValidator:
    def validate_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload  # Retorna los datos del usuario si el token es válido
        except InvalidTokenError:
            return None  # Retorna None si el token es inválido o ha expirado
