"""Module for member schema."""

from marshmallow import fields, pre_load, ValidationError
from ..utilities.helpers.schemas import common_args
from ..utilities.messages.error_messages import serialization_errors

from .base_schemas import AuditableBaseSchema
from ..models import Member, User
from .user import UserSchema
from ..utilities.constants import EXCLUDED_FIELDS


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


class MemberListSchema(AuditableBaseSchema):

    """Member schema to list members in
    a specific group"""

    user_id = fields.String(**common_args())
    user = fields.Method('get_user')

    def get_user(self, obj):
        """Function that returns user details"""
        # EXCLUDED_FIELDS.extend(['password'])
        user = User.get_or_404(obj.user_id)
        user_schema = UserSchema(exclude=EXCLUDED_FIELDS)
        return user_schema.dump(user)

    class Meta:
        """class Meta."""
        model = Member
        load_instance = True
