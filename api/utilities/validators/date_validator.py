from datetime import datetime
import dateutil.parser
from ..error import raises


def date_validator(date_value):
    """Validates date format

     Arguments:
        date_value (string): date string

     Raises:
        ValidationError: Used to raise exception if date format is not valid

    Returns:
        date: the validated date
    """

    try:
        dateutil.parser.parse(date_value).date()
        try:
            date = datetime.strptime(date_value, '%Y-%m-%d')
        except ValueError:
            raises('invalid_date', 400, date_value)
    except ValueError as error:
        # raise error if the date values are out of range
        raises('invalid_provided_date', 400, str(error))

    return date
