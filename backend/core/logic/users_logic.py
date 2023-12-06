from typing import TYPE_CHECKING, Tuple
from copy import copy

if TYPE_CHECKING:
    from ..shared.transaction import Transaction

from .sessions_logic import SessionsLogic
from ..shared.models import User, Session
from ..db.users_db import UsersDB


class UsersLogic():
    def __init__(self, transaction: "Transaction"):
        self.transaction = transaction
        self.db: UsersDB = UsersDB(transaction)

    def add(self, user: User) -> Tuple[User, Session]:
        new_user = copy(user)
        new_user.user_id = None

        self.db.add(new_user)

        self.transaction.current_user = new_user

        sessions_logic = SessionsLogic(self.transaction)
        session = sessions_logic.create(new_user.user_id)
        self.transaction.current_session = session

        return new_user, session

    def get(self, user_id: int) -> User:
        user = self.db.get(user_id)
        if user is None:
            raise Exception("User not found")

        return user

    def update(self, user: User) -> User:
        self.db.update(user)
        return user

    def login(self, username: str, password: str) -> Tuple[User, Session]:
        user = self.db.get_by_username(username)
        if not user or user.password != password:
            raise Exception("Username is not found or password is incorrect")

        self.transaction.current_user = user

        sessions_logic = SessionsLogic(self.transaction)
        session = sessions_logic.create(user.user_id)
        self.transaction.current_session = session

        return user, session
