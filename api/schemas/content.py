"""Group schema module."""

from marshmallow import fields, post_load

from .base_schemas import AuditableBaseSchema
from ..utilities.helpers.schemas import common_args
from ..models import Content
from ..utilities.validators.url_validator import url_validator


class ContentSchema(AuditableBaseSchema):
    """Content Schema."""
    content_url = fields.String(**common_args(validate=url_validator),
                              load_from='imageUrl',
                              dump_to='imageUrl')
    group_id = fields.String(**common_args())


    class Meta:
        """class Meta."""
        model = Content
        load_instance = True
