from flask_login import UserMixin
from admin import get_db

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        cur = db.execute(
            "SELECT id, username FROM admin WHERE id = ?",
            (user_id,)
        )
        row = cur.fetchone()
        db.close()

        if row:
            return User(row["id"], row["username"])
        return None
