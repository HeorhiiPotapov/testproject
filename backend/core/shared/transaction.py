from typing import Union, cast
import sqlite3

from .config import CONFIG
from .models import User, Session
from ..logic.users_logic import UsersLogic
from ..logic.sessions_logic import SessionsLogic


def dict_factory(cursor, row):
    return {cursor.description[i][0]: row[i] for i in range(len(cursor.description))}


class Transaction:
    def __init__(self, session_token: Union[str, None] = None,
                 allow_no_token: bool = False):

        self.connection = sqlite3.connect(CONFIG.db_path)
        self.connection.row_factory = dict_factory
        self.current_user: Union[User, None] = None
        self.current_session: Union[Session, None] = None

        if not session_token and not allow_no_token:
            raise Exception("No session token provided")

        if session_token:
            self.current_session = SessionsLogic(self).get_by_token(
                session_token)
            self.current_user = UsersLogic(self).get(
                cast(int, self.current_session.user_id))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.rollback()
        except:
            pass

        try:
            self.connection.close()
        except:
            pass

    def cursor(self):
        return self.connection.cursor()

    def rollback(self):
        self.connection.rollback()

    def commit(self):
        self.connection.commit()
