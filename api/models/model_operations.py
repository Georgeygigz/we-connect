
"""Module for generic model operations mixin."""

from datetime import datetime, timedelta
from flask import request

import jwt
from marshmallow import ValidationError as MarshmallowError

from config import AppConfig
from api.utilities.dynamic_filter import DynamicFilter
from api.utilities.validators.sorting_order_by_validator import validate_order_by_args

# middlewares
from ..middlewares.base_validator import ValidationError
from ..utilities.helpers.hash import verify_pin
from ..utilities.messages.error_messages import serialization_errors
from .database import db



class ModelOperations(object):

    """Mixin class with generic model operations."""
    def save(self):
        """Save a model instance."""
        if request and request.decoded_token:
            self.created_by = request.decoded_token.get('id')
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

            if cls.__name__ == 'User':
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
    def query_(cls, filter_condition=None, include_deleted=False):
        """
        Returns filtered database entries. It takes model class and
        filter_condition and returns database entries based on the filter
        condition, eg, User.query_('name,like,john'). Apart from 'like', other
        comparators are eq(equal to), ne(not equal to), lt(less than),
        le(less than or equal to) gt(greater than), ge(greater than or equal to)
        :param filter_condition:
        :return: an array of filtered records
        """
        if filter_condition:
            sort = cls.sorting_helper(filter_condition)
            dynamic_filter = DynamicFilter(cls)
            return dynamic_filter.filter_query(filter_condition).order_by(sort)

        sort = cls.sorting_helper()

        # return all results from the database, including
        # results flagged as deleted
        if include_deleted:
            return cls.query.include_deleted().order_by(sort)
        # import pdb; pdb.set_trace()
        return cls.query.order_by(sort)

    @classmethod
    def sorting_helper(cls, args={}):
        """
        Sort records of a model.

        Arguments:
            model (class): Model to be sorted
            args (dict): dictionary with sort query parameters

        Operations:
            1. convert sorting column to from camelCase to snake_case
            2. validate the sorting column exists in the model
            3. validate order_by value to be either asc or desc
            4. check if type of column is of json type then cast json to string
            4. map order_by to the respective sorting method

        Returns:
            (func) -- Returns function with sort by and order by
                      example:  "model.id.desc()"
        """
        # QueryParser imported here to avoid import loop
        from api.utilities.query_parser import QueryParser
        from sqlalchemy.types import String

        sort_column = QueryParser.to_snake_case(args.get("sort", "created_at"))
        sort_by = QueryParser.validate_column_exists(cls, sort_column)
        order_by = validate_order_by_args(args.get("order", "desc").lower())
        sorting_mapper = {"asc": sort_by.asc, "desc": sort_by.desc}

        # This will allow sorting of JSON column as String.
        if str(sort_by.type) == 'JSON':
            return sort_by.cast(String)

        return sorting_mapper[order_by]()

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
    def get_or_404(cls, id):
        """Return the record with id = id

        Args:
            cls (class): The user model class
            id (string): token_id of the user
        Returns:
            record (object): the user object which has id = token_id
        """
        record = cls.query.filter_by(id=id, deleted=False).first()
        if not record:
            raise ValidationError({'message': f'{cls.__name__ } not found'},
                                  404)
        return record

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
