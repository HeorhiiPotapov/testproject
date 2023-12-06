from typing import TYPE_CHECKING, Union, cast

if TYPE_CHECKING:
    from ..shared.transaction import Transaction

from ..shared.models import User, UserSchema


class UsersDB():
    def __init__(self, transaction: "Transaction"):
        self.transaction = transaction

    def get_by_username(self, username: str) -> Union[User, None]:
        query = ("SELECT user_id, username, first_name, last_name, "
                 "fav_color "
                 "FROM users "
                 "WHERE username = ?")

        cursor = self.transaction.cursor()
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            schema = UserSchema()
            return cast(User, schema.load(row))

        return None

    def get(self, user_id: int) -> Union[User, None]:
        query = ("SELECT user_id, username, first_name, last_name, fav_color "
                 "FROM users "
                 "WHERE user_id = ?")

        cursor = self.transaction.cursor()
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            schema = UserSchema()
            return cast(User, schema.load(row))

        return None

    def add(self, user: User):
        query = ("INSERT INTO users (username, first_name, last_name, "
                 "password, fav_color "
                 "VALUES (?, ?, ?, ?, ?)")
        cursor = self.transaction.cursor()
        cursor.execute(
            query,
            (user.username, user.first_name, user.last_name, user.password,
             user.fav_color))
        if cursor.lastrowid is not None:
            user.user_id = cursor.lastrowid
        cursor.close()

    def update(self, user: User):
        query = ("UPDATE users "
                 "SET username = ?, first_name = ?, last_name = ?, "
                 "fav_colour = ? "
                 "WHERE user_id = ?")
        cursor = self.transaction.cursor()
        cursor.execute(
            query,
            (user.username, user.first_name, user.last_name, user.fav_color,
             user.user_id))

        cursor.close()
