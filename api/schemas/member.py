"""Module for member schema."""

from marshmallow import fields, pre_load, ValidationError
from ..utilities.helpers.schemas import common_args
from ..utilities.messages.error_messages import serialization_errors

from .base_schemas import AuditableBaseSchema
from ..models import Member


class MemberSchema(AuditableBaseSchema):
    """Member Schema."""
    group_id = fields.String(**common_args())
    user_id = fields.String(**common_args())

    @pre_load
    def validate_member(cls, data, **kwargs):
        """Function that checks member already exist
        in a certain group

        Args:
            None
        """
        member = Member.query_().filter_by(user_id=data['user_id'],
                               group_id=data['group_id']).first()
        if member:
            raise ValidationError('You already exist in the group')
        return data

    class Meta:
        """class Meta."""
        model = Member
        load_instance = True