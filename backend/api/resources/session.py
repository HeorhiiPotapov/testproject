from typing import cast
from flask.views import MethodView
from flask import request

from core.sessions import get
from core.shared.config import CONFIG

from ..shared.utils import (success_response, error_reponse,
                            session_data_dict, get_session_token)


class Session(MethodView):
    def get(self):
        try:
            token = get_session_token()

            user, session = get(token)

            response = success_response(
                data=session_data_dict(user, session))

            return response
        except Exception as e:
            return error_reponse(e)
