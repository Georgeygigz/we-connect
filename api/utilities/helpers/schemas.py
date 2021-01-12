"""Helper functions for schemas."""

# Messages
from ..messages.error_messages import serialization_errors


def common_args(**kwargs):
    """Returns the common arguments used in marshmallow fields.

    Args:
        kwargs: key word arguments use in fields
        ie validate=some_function

    Returns:
        dict: Resultant fields to be passed to a schema

    """
    return {
        "required": True,
        "validate": kwargs.get('validate'),
        "error_messages": {
            'required': serialization_errors['field_required']
        }
    }
