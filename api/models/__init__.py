from sqlalchemy import event

from .push_id import PushID
from .user import User


def fancy_id_generator(mapper, connection, target):
    """A function to generate unique identifiers on insert."""
    push_id = PushID()
    target.id = push_id.next_id()


tables = [User]

for tables in tables:
    event.listen(tables, 'before_insert', fancy_id_generator)
