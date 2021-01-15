
# System imports

from .base.auditable_model import AuditableBaseModel
from .database import db


class User(AuditableBaseModel):

    """"Class for user db table"""
    policies = {'patch': None, 'delete': 'owner'}

    __tablename__ = 'users'

    name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=False)

    def get_child_relationships(self):

        """Method to get all child relationships a model has. Overide in the
        subclass if the model has child models.
        """
        return None

    def __repr__(self):
        return f'<User {self.name}>'
