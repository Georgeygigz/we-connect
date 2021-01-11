
"""Module that handles jwt token generation and decoding."""

import jwt

from config import AppConfig

from ...middlewares.base_validator import ValidationError
from ...models import User
from ...utilities.messages.error_messages import jwt_errors


def get_token_data(token):
    """Checks validity of a token

    Args:
        token (str): token to be validated
    Return:
        user (obj): valid user object
    """
    try:
        payload = jwt.decode(
            token, AppConfig.SECRET_KEY, algorithms="HS256")
        user = User.get_or_404(payload['id'])
    except Exception as error:
        exception_mapper = {
            jwt.ExpiredSignatureError: jwt_errors['token_expired'],
            jwt.DecodeError: jwt_errors['invalid_token'],
            jwt.InvalidIssuerError: jwt_errors['invalid_secret'],
            User.DoesNotExist: jwt_errors['token_user_not_found']
        }
        message, status_code = exception_mapper.get(
            type(error), 'Authorization failed.', 400)
        raise ValidationError({'message': message}, status_code)

    return user
