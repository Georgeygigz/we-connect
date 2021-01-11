from marshmallow import fields, post_load

from ..models import User
from ..schemas.base_schemas import AuditableBaseSchema
from ..utilities.helpers.hash import hash_pin
from ..utilities.helpers.schemas import common_args
from ..utilities.validators.email_validator import email_validator
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.string_length_validators import \
    string_length_validator
from ..utilities.validators.url_validator import url_validator


class UserSchema(AuditableBaseSchema):

    """Role model schema."""
    name = fields.String(
        **common_args(validate=[string_length_validator(6), name_validator]), )
    username = fields.String(**common_args(
        validate=[string_length_validator(60), name_validator]))
    email = fields.String(**common_args(validate=email_validator))
    password = fields.String(**common_args(
        validate=[string_length_validator(100), name_validator]))
    image_url = fields.String(**common_args(validate=url_validator),
                              load_from='imageUrl',
                              dump_to='imageUrl')

    @post_load
    def hash_password(cls, data, **kwargs):
        """Hash password to ensure security

        Args:
            data(dict): json data
        Return:
            data(dict): json data with hashed password
        """
        data['password'] = hash_pin(data['password'])
        return data

    class Meta:

        """class Meta."""
        model = User
        load_instance = True


class LoginSchema(AuditableBaseSchema):

    """Login schema."""
    email = fields.String(**common_args(validate=email_validator))
    password = fields.String(**common_args(
        validate=[string_length_validator(100), name_validator]))
