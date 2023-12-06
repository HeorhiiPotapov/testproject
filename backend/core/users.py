from typing import Tuple, cast

from .shared.models import User, Session
from .logic.users_logic import UsersLogic
from .shared.transaction import Transaction


def signup(user: User) -> Tuple[User, Session]:
    with Transaction(allow_no_token=True) as transaction:
        logic = UsersLogic(transaction)
        new_user, session = logic.add(user)
        transaction.commit()

    return new_user, session


def login(username: str, password: str) -> Tuple[User, Session]:
    with Transaction(allow_no_token=True) as transaction:
        logic = UsersLogic(transaction)
        new_user, session = logic.login(username, password)
        transaction.commit()

    return new_user, session


def get(token: str) -> User:
    with Transaction(session_token=token) as transaction:
        logic = UsersLogic(transaction)
        user = logic.get(
            cast(int, cast(User, transaction.current_user).user_id))

    return user


def update(user: User, token: str) -> User:
    with Transaction(session_token=token) as transaction:
        logic = UsersLogic(transaction)
        updated_user = logic.update(user)

    return updated_user
