from sqlalchemy import event

from .push_id import PushID
from .user import User
from .group import Group
from .member import Member
from .content import Content


def fancy_id_generator(mapper, connection, target):
    """A function to generate unique identifiers on insert."""
    push_id = PushID(20,12)
    target.id = push_id.next_id()


tables = [User, Group, Member, Content]

for tables in tables:
    event.listen(tables, 'before_insert', fancy_id_generator)
