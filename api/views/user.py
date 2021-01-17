
from flask import request
from flask_restx import Resource

from ..models import User
from ..schemas.user import LoginSchema, UserSchema
from ..utilities.constants import EXCLUDED_FIELDS
from ..utilities.helpers.token import get_token_data
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.swagger.collections.user import user_namespace
from ..utilities.validators.validate_json_request import validate_json_request


@user_namespace.route('/signup')
class UserResource(Resource):

    """User Resource class for creating and getting users."""
    @validate_json_request
    def post(self):
        """Creates a user

        Returns:
            (dict): Returns status and success message
            data(dict): Returns the user data
        """
        request_data = request.get_json()
        user_schema = UserSchema(exclude=EXCLUDED_FIELDS)
        user_schema.context['request'] = request
        user_data = user_schema.load(request_data)
        user = User.find_or_create(user_data, email=request_data['email'])

        return (
            {
                "status": "success",
                "message": SUCCESS_MESSAGES["sign_up"],
                "data": user_schema.dump(user),
            },
            201,
        )


@user_namespace.route('/verify/<string:token>')
class VerifyUserResource(Resource):

    """Perform operation to a single user."""
    def get(self, token):
        """Verify user account"""
        user = get_token_data(token)
        user.is_active = True
        user.save()

        return (
            {
                "status": "success",
                "message": SUCCESS_MESSAGES["success"].format('Congratulation! email verified'),
                "data": user.email,
            },
            200,
        )


@user_namespace.route('/<string:user_id>')
class VerifyUserResource(Resource):

    """Perform operation to a single user."""
    def get(self, user_id):
        """Get single user"""
        user = User.get_or_404(user_id)
        user_schema = UserSchema(exclude=EXCLUDED_FIELDS)


        return (
            {
                "status": "success",
                "message": SUCCESS_MESSAGES["success"].format('Congratulation! email verified'),
                "data": user_schema.dump(user),
            },
            200,
        )



@user_namespace.route('/login')
class LoginResource(Resource):

    """User Resource class for creating and getting users."""
    def post(self):
        """Login a user

        Returns:
            None
        """
        request_data = request.get_json()
        user_schema = LoginSchema(exclude=EXCLUDED_FIELDS)
        user_schema.context['request'] = request
        user_data = user_schema.load(request_data)
        user = User.find_active_user(user_data)

        return (
            {
                "status": "success",
                "message": SUCCESS_MESSAGES["success"].format('Login'),
                "data": user,
            },
            200,
        )
