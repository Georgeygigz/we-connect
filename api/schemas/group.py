"""Group schema module."""

from marshmallow import fields, post_load

from .base_schemas import AuditableBaseSchema
from ..utilities.helpers.schemas import common_args
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.string_length_validators import \
    string_length_validator
from ..models.group import Group
from ..models.push_id import PushID


class GroupSchema(AuditableBaseSchema):

    """Group Schema."""
    group_name = fields.String(
        **common_args(validate=[string_length_validator(25),]))
    description = fields.String(**common_args(
        validate=[string_length_validator(60)]))
    group_code = fields.String(validate=[string_length_validator(25),])

    @post_load
    def generate_code(cls,data, **kwargs):
        """Generate group code

        Args:
            data(dict): json data
        Return:
            data(dict): json data with group code
        """
        push_id = PushID(8,4)
        group_code = push_id.next_id()
        data['group_code'] = group_code
        return data

    class Meta:

        """class Meta."""
        model = Group
        load_instance = True
