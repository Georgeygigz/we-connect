from flask import request
from flask_restx import Resource

from ..utilities.swagger.collections.content import content_namespace
from ..utilities.helpers.token import token_required
from ..schemas.content import ContentSchema, Content
from ..utilities.constants import EXCLUDED_FIELDS
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..models import Group


@content_namespace.route('/<string:group_id>')
class ContentResource(Resource):
    @token_required
    def post(self, group_id):
        """Create content."""
        request_data = request.get_json()

        # get group
        group = Group.get_or_404(group_id)
        request_data['group_id'] = group.id

        content_schema = ContentSchema(exclude=EXCLUDED_FIELDS)
        content_data = content_schema.load(request_data)
        content = Content.find_or_create(
            content_data, content_url=request_data['content_url'])

        return ({
            "status":
            "success",
            "message":
            SUCCESS_MESSAGES['success'].format('Content created'),
            "data":
            content_schema.dump(content)
        })
