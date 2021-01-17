"""Content module"""

from sqlalchemy.sql import select

from .base.auditable_model import AuditableBaseModel
from .database import db
from . import Group


class Content(AuditableBaseModel):

    """Class for content table"""

    __tablename__ = 'content'
    content_url = db.Column(db.String)

    group_id = db.Column(
        db.String,
        db.ForeignKey('group.id'),
        nullable=False,)

    def __repr__(self):
        group = Group.get_or_404(self.group_id)
        return f'<Contents of {group.group_name}>'
