
"""A module for raising errors."""

from marshmallow import ValidationError as MarshmallowError

from api.middlewares.base_validator import ValidationError

from .messages.error_messages import serialization_errors


def raises(error_key, status_code, *args, **kwargs):
    """Raises a serialization error

    Parameters:
        error_key (str): the key for accessing the correct error message
        args (*): variable number of arguments
        kwargs (**): variable number of keyword arguments
    """

    raise ValidationError(
        {
            'message': serialization_errors[error_key].format(*args, **kwargs)
        }, status_code)


def raise_error(error_key, *args, **kwargs):
    """Raises a Marshmallow validation error

    Args:
        error_key (str): The key for accessing the correct error message
        *args: Arguments taken by the serialization error message
        **kwargs:
            fields (list): The fields where the error will appear

    Raises:
        ValidationError: Marshmallow validation error
    """
    raise MarshmallowError(serialization_errors[error_key].format(*args),
                           kwargs.get('fields'))
