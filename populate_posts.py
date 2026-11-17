
from database import get_connection


def populate_posts():
    connection = get_connection()

    posts = [
        (
            "SQL Basics",
            "An introduction to SQL queries and databases.",
            "alice"
        ),
        (
            "Flask Security",
            "Understanding authentication and application security.",
            "alice"
        ),
        (
            "Database Design",
            "Understanding tables, relationships and foreign keys.",
            "bob"
        )
    ]

    for title, content, username in posts:

        # Find the user associated with the post
        user = connection.execute("""
            SELECT id FROM users
            WHERE username = ?
        """, (username,)).fetchone()

        if user is None:
            print(f"User '{username}' not found. Skipping post.")
            continue

        # Check whether the post already exists
        existing_post = connection.execute("""
            SELECT id FROM posts
            WHERE title = ? AND user_id = ?
        """, (title, user["id"])).fetchone()

        if existing_post is None:
            connection.execute("""
                INSERT INTO posts (title, content, user_id)
                VALUES (?, ?, ?)
            """, (title, content, user["id"]))

    connection.commit()
    connection.close()

    print("Posts populated successfully.")


if __name__ == "__main__":
    populate_posts()


