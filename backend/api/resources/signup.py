from typing import cast
from flask.views import MethodView
from flask import request

from core.shared.models import UserSchema, User, Casing
from core.users import signup
from core.shared.config import CONFIG

from ..shared.utils import success_response, error_reponse, session_data_dict


class Signup(MethodView):
    def post(self):
        try:
            if not request.is_json:
                raise Exception("Request is not JSON")

            json_data = request.data.decode("utf-8")
            schema = UserSchema(external_casing=Casing.CAMEL)
            user: User = cast(User, schema.loads(json_data))
            new_user, session = signup(user)

            response = success_response(
                data=session_data_dict(new_user, session))

            response.set_cookie(
                "sessionToken",
                cast(str, session.token),
                httponly=True,
                max_age=CONFIG.session_timeout_seconds)

            return response
        except Exception as e:
            return error_reponse(e)
