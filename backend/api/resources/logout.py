from flask.views import MethodView

from core.sessions import logout

from ..shared.utils import success_response, error_reponse, get_session_token


class Logout(MethodView):
    def post(self):
        try:
            token = get_session_token()

            logout(token)

            response = success_response()
            response.set_cookie("sessionToken", "", httponly=True, expires=0)
            return response
        except Exception as e:
            return error_reponse(e)
