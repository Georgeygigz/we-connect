"""Module for signup user endpoint."""

import json

from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from config import AppConfig


class TestSignUpUser:

    """Test endpoint for signing up a newuser."""
    def test_signup_new_user_succeeds(self, init_db, client, user_signup):
        """Should return an 201 status code and success message when a

        user is created in request is valid
        Parameters:
            init_db(object): fixture to initialize the test database
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
            user_signup(object): fixture to signup new user
        """
        user_data = {
            "name": "George",
            "username": "Muttii",
            "email": "georgeymutti@gmail.com",
            "password": "Geoerge",
            "image_url": "https://img.png"
        }
        response = client.post(
            f'{AppConfig.AUTH_URL}signup', data=json.dumps(user_data),
            headers={'Content-Type': 'application/json'})

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES["sign_up"].format(
            'Congratulation! email verified')

    def test_signup_new_user_without_email_fails(self, init_db, client, user_signup):
        """Should return an 201 status code and success message when a

        user is created in request is valid
        Parameters:
            init_db(object): fixture to initialize the test database
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
            user_signup(object): fixture to signup new user
        """
        user_data = {
            "name": "George",
            "username": "Muttii",
            "password": "Geoerge",
            "image_url": "https://img.png"
        }
        response = client.post(
            f'{AppConfig.AUTH_URL}signup', data=json.dumps(user_data),
            headers={'Content-Type': 'application/json'})

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'failed'
        assert isinstance(response_json['errors'], list)
        assert response_json['errors'][0] == 'email this field is required'
