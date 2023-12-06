from typing import cast
from flask.views import MethodView
from flask import request

from core.users import get, update

from core.shared.models import User as UserClass, UserSchema, Casing

from ..shared.utils import success_response, error_reponse, get_session_token


class User(MethodView):
    def get(self):
        try:
            token = get_session_token()

            user = get(token)

            schema = UserSchema()
            user_dict: dict = cast(dict, schema.dump(user))

            return success_response(data=user_dict,
                                    convert_keys_to_camel=True)

        except Exception as e:
            return error_reponse(e)

    def put(self):
        try:
            token = get_session_token()

            if not request.is_json:
                raise Exception("Request is not JSON")
            json_data = request.data.decode("utf-8")
            print(json_data)
            schema = UserSchema(external_casing=Casing.CAMEL)
            user: UserClass = cast(UserClass, schema.loads(json_data))
            updated_user = update(user, token)
            schema = UserSchema()
            updated_user_dict: dict = cast(dict, schema.dump(updated_user))

            return success_response(data=updated_user_dict,
                                    convert_keys_to_camel=True)

        except Exception as e:
            return error_reponse(e)
