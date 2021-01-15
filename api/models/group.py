from .base.auditable_model import AuditableBaseModel
from .database import db


class Group(AuditableBaseModel):

    """Class for groups user db table"""
    policies = {'patch':None, 'delete': 'owner'}

    __tablename__ = 'group'
    group_name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.Text, nullable=False)
    group_code = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<User {self.group_name}>'