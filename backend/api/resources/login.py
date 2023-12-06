from typing import cast
from flask import request
from flask.views import MethodView
from marshmallow import Schema, fields

from core.users import login
from core.shared.config import CONFIG

from ..shared.utils import success_response, error_reponse, session_data_dict


class Login(MethodView):
    class PostSchema(Schema):
        username = fields.Str(required=True)
        password = fields.Str(required=True)

    def post(self):
        try:
            if not request.is_json:
                raise Exception("Request is not JSON")

            json_data = request.data.decode("utf-8")
            schema = Login.PostSchema()
            data = cast(dict[str, str], schema.loads(json_data))
            user, session = login(data["username"], data["password"])

            response = success_response(
                data=session_data_dict(user, session))

            response.set_cookie(
                "sessionToken",
                cast(str, session.token),
                httponly=True,
                max_age=CONFIG.session_timeout_seconds)

            return response

        except Exception as e:
            return error_reponse(e)
