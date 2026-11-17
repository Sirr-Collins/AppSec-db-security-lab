from database import get_connection
from werkzeug.security import generate_password_hash


def add_user():
    connection = get_connection()

    connection.execute("""
        INSERT OR IGNORE INTO users
        (username, password_hash, email)
        VALUES (?, ?, ?)
    """, (
        "charlie",
        generate_password_hash("CharliePassword123!"),
        "charlie@example.com"
    ))

    connection.commit()
    connection.close()

    print("Charlie added successfully.")


if __name__ == "__main__":
    add_user()