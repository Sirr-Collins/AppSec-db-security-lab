from werkzeug.security import check_password_hash

from database import get_connection

connection = get_connection()

user = connection.execute(
    "SELECT * FROM users WHERE username = ?",
    ("alice",)
).fetchone()

if user:
    print("Username found:", user["username"])

    result = check_password_hash(
        user["password_hash"],
        "AlicePassword123!"
    )

    print("Password matches:", result)
else:
    print("User not found")

connection.close()