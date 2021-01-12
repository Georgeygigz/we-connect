"""Module for generic string length validators."""

from ..error import raise_error


def string_length_validator(length):
    """Returns a function that checks data over a given length

    Args:
        length (Integer): Length a string must not exceed
    Returns:
        Function which validates length of the data
    """
    def length_validator(data):
        """Checks if data does not exceed a given length

        Args:
            data (String): data to be validated
        Raises:
            validation error if data exceeds a given length
        """
        if len(data) > length:
            raise_error('string_length', length, fields=data)

    return length_validator
