from typing import Tuple, cast

from .shared.models import User, Session
from .shared.transaction import Transaction
from .logic.sessions_logic import SessionsLogic


def get(token: str) -> Tuple[User, Session]:
    with Transaction(session_token=token) as transaction:
        return (cast(User, transaction.current_user),
                cast(Session, transaction.current_session))


def logout(token: str):
    with Transaction(session_token=token) as transaction:
        logic = SessionsLogic(transaction)
        logic.logout()
        transaction.commit()
