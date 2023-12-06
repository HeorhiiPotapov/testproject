from secrets import token_urlsafe
from hashlib import sha256
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..shared.transaction import Transaction

from ..shared.models import Session
from ..shared.config import CONFIG
from ..db.sessions_db import SessionsDB


class SessionsLogic():
    def __init__(self, transaction: "Transaction"):
        self.transaction = transaction
        self.db = SessionsDB(transaction)

    def create(self, user_id) -> Session:
        token = token_urlsafe(CONFIG.token_length)
        hashed_token = sha256(token.encode("UTF-8")).hexdigest()
        session = Session(user_id=user_id)
        session.token = hashed_token
        self.db.add(session)
        session.token = token
        return session

    def get_by_token(self, token: str) -> Session:
        session = self.db.get_by_token(token)
        if session is None:
            raise Exception("Session token is not valid")

        return session

    def delete(self, session: Session):
        self.db.delete(session)

    def logout(self):
        if self.transaction.current_session:
            self.db.delete(self.transaction.current_session)
            self.transaction.current_session = None
