"""Module for setting up users fixtures."""

import pytest

from api.models import User


@pytest.fixture(scope='function')
def user_signup(app):
    user = User(
        name='George',
        username='Mutti',
        email='georgeymutti@gmail.com',
        password="password"
    )
    return user
