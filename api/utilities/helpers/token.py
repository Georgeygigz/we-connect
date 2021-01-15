
"""Module that handles jwt token generation and decoding."""

import jwt
from functools import wraps

from flask import request
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


def get_token(http_request=request):
    """Get token from request object

    Args:
        http_request (HTTPRequest): Http request object

    Returns:
        token (string): Token string

    Raises:
        ValidationError: Validation error raised when there is no token
                         or bearer keyword in authorization header
    """
    token = http_request.headers.get('Authorization')
    if not token:
        raise ValidationError({'message': jwt_errors['NO_TOKEN_MSG']}, 401)
    elif 'bearer' not in token.lower():
        raise ValidationError({'message': jwt_errors['NO_BEARER_MSG']}, 401)
    token = token.split(' ')[-1]
    return token


def token_required(func):
    """Authentication decorator. Validates token from the client

    Args:
        func (function): Function to be decorated

    Returns:
        function: Decorated function

    Raises:
        ValidationError: Validation error
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = get_token()
        try:
            secret_key = AppConfig.SECRET_KEY

            decoded_token = jwt.decode(
                token,
                secret_key,
                algorithms=['HS256'],
                options={
                    'verify_signature': True,
                    'verify_exp': True
                })
        except jwt.exceptions.InvalidAudienceError:
            decoded_token = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience='andela.com',
                issuer="accounts.andela.com")
        except (
                ValueError,
                TypeError,
                jwt.ExpiredSignatureError,
                jwt.DecodeError,
                jwt.InvalidSignatureError,
                jwt.InvalidAlgorithmError,
                jwt.InvalidIssuerError,
        ) as error:
            exception_mapper = {
                ValueError: (jwt_errors['SERVER_ERROR_MESSAGE'], 500),
                TypeError: (jwt_errors['SERVER_ERROR_MESSAGE'], 500),
                jwt.ExpiredSignatureError: (jwt_errors['EXPIRED_TOKEN_MSG'],
                                            401),
                jwt.DecodeError: (jwt_errors['INVALID_TOKEN_MSG'], 401),
                jwt.InvalidIssuerError: (jwt_errors['ISSUER_ERROR'], 401),
                jwt.InvalidAlgorithmError: (jwt_errors['ALGORITHM_ERROR'],
                                            401),
                jwt.InvalidSignatureError: (jwt_errors['SIGNATURE_ERROR'], 500)
            }
            message, status_code = exception_mapper.get(
                type(error), (jwt_errors['SERVER_ERROR_MESSAGE'], 500))
            raise ValidationError({'message': message}, status_code)

        # setting the payload to the request object and can be accessed with \
        # request.decoded_token from the view
        setattr(request, 'decoded_token', decoded_token)
        return func(*args, **kwargs)

    return decorated_function
