"""Member module"""

from sqlalchemy.sql import select

from ..middlewares.base_validator import ValidationError
from ..utilities.messages.error_messages import serialization_errors
from .base.auditable_model import AuditableBaseModel
from .database import db
from . import User, Group


class Member(AuditableBaseModel):

    """Class for groups user db table"""
    policies = {'patch':None, 'delete': 'owner'}

    __tablename__ = 'member'
    user_id = db.Column(
        db.String,
        db.ForeignKey('users.id'),
        nullable=False)

    group_id = db.Column(
        db.String,
        db.ForeignKey('group.id'),
        nullable=False,)

    def __repr__(self):
        group = Group.get_or_404(self.group_id)
        return f'<Members of {group.group_name}>'
