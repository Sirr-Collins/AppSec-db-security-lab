
from database import get_connection
from werkzeug.security import generate_password_hash


def initialize_database():
    connection = get_connection()

    # Create users table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)

    # Create posts table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Create employees table
    connection.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

    # Create test accounts
    users = [
        (
            "alice",
            generate_password_hash("AlicePassword123!"),
            "alice@example.com"
        ),
        (
            "bob",
            generate_password_hash("BobPassword123!"),
            "bob@example.com"
        ),
        (
            "charlie",
            generate_password_hash("CharliePassword123!"),
            "charlie@example.com"
        )
    ]

    connection.executemany("""
        INSERT OR IGNORE INTO users
        (username, password_hash, email)
        VALUES (?, ?, ?)
    """, users)

    # Add sample employees without creating duplicates
    employees = [
        ("David", "IT"),
        ("Sarah", "Finance")
    ]

    for name, department in employees:
        connection.execute("""
            INSERT INTO employees (name, department)
            SELECT ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM employees
                WHERE name = ? AND department = ?
            )
        """, (name, department, name, department))

    connection.commit()
    connection.close()

    print("Database initialized successfully.")


if __name__ == "__main__":
    initialize_database()
