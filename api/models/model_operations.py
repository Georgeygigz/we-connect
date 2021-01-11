
"""Module for generic model operations mixin."""

from datetime import datetime, timedelta

import jwt
from marshmallow import ValidationError as MarshmallowError

from config import AppConfig

# middlewares
from ..middlewares.base_validator import ValidationError
from ..utilities.helpers.hash import verify_pin
from ..utilities.messages.error_messages import serialization_errors
from .database import db


class ModelOperations(object):

    """Mixin class with generic model operations."""
    def save(self):
        """Save a model instance."""
        # if request and request.decoded_token:
        #     self.created_by = request.decoded_token.get('UserInfo').get('id')
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_or_create(cls, data, **kwargs):
        """Finds a model instance or creates it."""
        from api.tasks.email_sender import Email
        instance = cls.query.filter_by(**kwargs).first()
        if not instance:
            instance = cls(**data).save()
            # generate token
            token = cls.token(instance)['token']

            template_data = {
                'link': f'{AppConfig.VERIFY_URL}/{token}',
                'first_name': data['username']
            }
            # Email.send_mail.delay('Tile', [data['email']], 'Hello')
            Email.send_mail_with_template.delay('Verify Email',
                                                [data['email']], 'verify.html',
                                                template_data)
        return instance

    @classmethod
    def find_active_user(cls, data, **kwargs):
        """Finds active user and log then in."""
        # check if the user email is existing
        instance = cls.query.filter_by(email=data['email'],
                                       is_active=True).first()
        if not instance:
            raise MarshmallowError(serialization_errors['user_not_found'])

        # validate password
        is_password_correct = verify_pin(data['password'], instance.password)
        if not is_password_correct:
            raise MarshmallowError(serialization_errors['user_not_found'])
        return cls.token(instance)

    @classmethod
    def get_or_404(cls, token_id):
        """Return the user with id = token_id

        Args:
            cls (class): The user model class
            id (string): token_id of the user
        Returns:
            user (object): the user object which has id = token_id
        """
        user = cls.query.filter_by(id=token_id, deleted=False).first()
        if not user:
            raise ValidationError({'message': f'{cls.__name__ } not found'},
                                  404)
        return user

    @classmethod
    def token(cls, obj):
        """This method generates and returns a string of the token generated."""
        date = datetime.now() + timedelta(hours=int(AppConfig.TOKEN_EXP_TIME))

        payload = {
            'email': obj.email,
            'exp': int(date.strftime('%s')),
            'id': obj.id,
            "username": obj.username
        }
        token = jwt.encode(payload, AppConfig.SECRET_KEY, algorithm='HS256')
        payload = {'email': obj.email, 'token': token}

        return payload
