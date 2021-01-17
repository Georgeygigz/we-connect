from flask import request
from flask_restx import Resource

from ..models import Group, User, Member
from ..schemas.group import GroupSchema
from ..schemas.member import MemberSchema, MemberListSchema
from ..utilities.constants import EXCLUDED_FIELDS
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.swagger.collections.group import group_namespace
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.helpers.token import token_required


@group_namespace.route('/')
class GroupResource(Resource):

    @token_required
    @validate_json_request
    def post(self):
        """Create group

        Returns:
            (dict): Returns status and success message
            data(dict): Returns the id, title and description of the group created
        """
        request_data = request.get_json()
        group_schema = GroupSchema(exclude=EXCLUDED_FIELDS)
        group_schema.context['request'] = request
        group_data = group_schema.load(request_data)
        group = Group.find_or_create(group_data,
                                     group_name=request_data['group_name'])

        return (
            {
                "status": "success",
                "message": SUCCESS_MESSAGES["success"].format('Group'),
                "data": group_schema.dump(group),
            },
            201,
        )

    @token_required
    def get(self):
        """Get all groups."""

        group_schema = GroupSchema(
            many=True,
            exclude=EXCLUDED_FIELDS,
        )
        groups = Group.query_().all()

        return (
            {
                "status": "success",
                "message":
                SUCCESS_MESSAGES["success"].format('Groups retrieved'),
                "data": group_schema.dump(groups),
            },
            201,
        )


@group_namespace.route('/<string:id>')
class SingleGroupResource(Resource):

    """Resource to get single group"""
    @token_required
    def get(self, id):
        group_schema = GroupSchema(exclude=EXCLUDED_FIELDS, )
        group = Group.get_or_404(id)

        return (
            {
                "status": "success",
                "message":
                SUCCESS_MESSAGES["success"].format('Group retrieved'),
                "data": group_schema.dump(group),
            },
            200,
        )


@group_namespace.route('/join/<string:group_id>')
class GroupJoinResource(Resource):

    """Resource to join a new group"""
    @token_required
    def get(self, group_id):
        token_id = request.decoded_token.get('id')
        group = Group.get_or_404(group_id)
        user = User.get_or_404(token_id)
        data = {'group_id':group.id, 'user_id':user.id}

        # schema
        member_schema = MemberSchema()
        member_data = member_schema.load(data)

        new_member = Member(**data)
        new_member.save()
        message = f"You have successfully joined {group.group_name}'s group"

        return (
            {
                "status": "success",
                "message": message,
            },
            200,
        )


@group_namespace.route('/members/<string:group_id>')
class GroupJoinResource(Resource):

    """Resource to get all members in a group"""
    @token_required
    def get(self, group_id):
        group = Group.get_or_404(group_id)
        members = Member.query_().filter_by(group_id=group.id)

        # schema
        member_schema = MemberListSchema(many=True, exclude=EXCLUDED_FIELDS)

        return (
            {
                "status": "success",
                "message": SUCCESS_MESSAGES['success'].format('Members'),
                "data": member_schema.dump(members)
            },
            200,
        )