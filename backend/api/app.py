from flask import Flask
from flask_cors import CORS

from .resources.login import Login
from .resources.logout import Logout
from .resources.session import Session
from .resources.signup import Signup
from .resources.user import User

_ROOT_PATH = "/jr-interview/v2/"


def create_app():
    app = Flask(__name__.split(".")[0], root_path="..")
    CORS(app, supports_credentials=True)

    app.add_url_rule(f"{_ROOT_PATH}login",
                     view_func=Login.as_view("login"),
                     methods=["POST"])

    app.add_url_rule(f"{_ROOT_PATH}logout",
                     view_func=Logout.as_view("logout"),
                     methods=["POST"])

    app.add_url_rule(f"{_ROOT_PATH}session",
                     view_func=Session.as_view("session"),
                     methods=["GET"])

    app.add_url_rule(f"{_ROOT_PATH}signup",
                     view_func=Signup.as_view("signup"),
                     methods=["POST"])

    app.add_url_rule(f"{_ROOT_PATH}user",
                     view_func=User.as_view("user"),
                     methods=["GET", "PUT"])

    return app
