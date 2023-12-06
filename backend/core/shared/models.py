from typing import Union
from enum import IntEnum

from marshmallow import Schema, post_load, fields, validate


class Casing(IntEnum):
    SNAKE = 1
    CAMEL = 2


class ModelSchema(Schema):
    def __init__(self, external_casing: Union[Casing, None] = None, **kwargs):
        self.external_casing = external_casing
        super().__init__(**kwargs)

    def on_bind_field(self, field_name, field_obj):
        if self.external_casing == Casing.CAMEL:
            def camelcase(s):
                parts = iter(s.split("_"))
                return next(parts) + "".join(i.title() for i in parts)

            field_obj.data_key = camelcase(field_obj.data_key or field_name)


class UserSchema(ModelSchema):
    user_id = fields.Integer(required=False, missing=None)
    username = fields.String(required=True, validate=validate.Length(1))
    first_name = fields.String(required=True, validate=validate.Length(1))
    last_name = fields.String(required=True, validate=validate.Length(1))
    password = fields.String(required=False, missing=None,
                             validate=validate.Length(1))
    fav_color = fields.String(required=True, validate=validate.Length(1))

    @post_load
    def make_user(self, data: dict, **kwargs):
        return User(**data)


class User():
    def __init__(self,
                 user_id: Union[int, None] = None,
                 username: Union[str, None] = None,
                 first_name: Union[str, None] = None,
                 last_name: Union[str, None] = None,
                 password: Union[str, None] = None,
                 fav_color: Union[str, None] = None,):

        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.fav_color = fav_color


class SessionSchema(ModelSchema):
    session_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    token = fields.String(required=True)

    @post_load
    def make_session(self, data, **kwargs):
        return Session(**data)


class Session():
    def __init__(self,
                 session_id: Union[int, None] = None,
                 user_id: Union[int, None] = None,
                 token: Union[str, None] = None):

        self.session_id = session_id
        self.user_id = user_id
        self.token = token
