from typing import TYPE_CHECKING, Union, cast

if TYPE_CHECKING:
    from ..shared.transaction import Transaction

from ..shared.models import Session, SessionSchema


class SessionsDB():
    def __init__(self, transaction: "Transaction"):
        self.transaction = transaction

    def add(self, session: Session):
        query = ("INSERT INTO sessions (user_id, token) "
                 "VALUES (?, ?)")
        cursor = self.transaction.cursor()
        cursor.execute(query, (session.user_id, session.token))
        if cursor.lastrowid is not None:
            session.session_id = cursor.lastrowid
        cursor.close()

    def get_by_token(self, token: str) -> Union[Session, None]:
        query = ("SELECT session_id, user_id, token "
                 "FROM sessions "
                 "WHERE token = ?")

        cursor = self.transaction.cursor()
        cursor.execute(query, (token,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            schema = SessionSchema()
            return cast(Session, schema.load(row))

        return None

    def delete(self, session: Session):
        query = "DELETE FROM sessions WHERE session_id = ?"
        cursor = self.transaction.cursor()
        cursor.execute(query, (session.session_id,))
        cursor.close()
