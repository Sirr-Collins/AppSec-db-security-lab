
from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash

from database import get_connection

app = Flask(__name__)


# VULNERABLE LOGIN ENDPOINT
@app.route("/vulnerable/login", methods=["POST"])
def vulnerable_login():

    data = request.get_json(silent=True) or request.form

    username = data.get("username", "")

    connection = get_connection()

    # INTENTIONALLY VULNERABLE
    query = (
        f"SELECT * FROM users "
        f"WHERE username = '{username}'"
    )

    user = connection.execute(query).fetchone()

    connection.close()

    if user:
        return jsonify({
            "message": "Login successful",
            "username": user["username"],
            "authentication_method": "SQL query result"
        }), 200

    return jsonify({
        "message": "Invalid username"
    }), 401



# SECURE LOGIN ENDPOINT
@app.route("/secure/login", methods=["POST"])
def secure_login():

    data = request.get_json(silent=True) or request.form

    username = data.get("username", "")
    password = data.get("password", "")

    connection = get_connection()

    # SECURE:
    # Parameterized query separates SQL instructions
    # from user-supplied values.
    query = """
        SELECT * FROM users
        WHERE username = ?
    """

    user = connection.execute(
        query,
        (username,)
    ).fetchone()

    connection.close()

    # Verifies the supplied password against the stored hash.
    if user and check_password_hash(
        user["password_hash"], password
    ):
        return jsonify({
            "message": "Login successful",
            "username": user["username"]
        }), 200

    return jsonify({
        "message": "Invalid username or password"
    }), 401



# VULNERABLE SEARCH ENDPOINT
@app.route("/vulnerable/search", methods=["POST"])
def vulnerable_search():

    data = request.get_json(silent=True) or request.form

    search_term = data.get("search_term", "")

    connection = get_connection()

    # INTENTIONALLY VULNERABLE:
    # User input is directly concatenated into SQL.
    query = (
        f"SELECT title, content FROM posts "
        f"WHERE title = '{search_term}'"
    )

    results = connection.execute(query).fetchall()

    connection.close()

    return jsonify([
        {
            "title": row["title"],
            "content": row["content"]
        }
        for row in results
    ]), 200



#SECURE SEARCH ENDPOINT
@app.route("/secure/search", methods=["POST"])
def secure_search():

    data = request.get_json(silent=True) or request.form

    search_term = data.get("search_term", "")

    connection = get_connection()

    # SAFE: Parameterized SQL query
    query = """
        SELECT title, content
        FROM posts
        WHERE title = ?
    """

    results = connection.execute(
        query,
        (search_term,)
    ).fetchall()

    connection.close()

    return jsonify([
        {
            "title": row["title"],
            "content": row["content"]
        }
        for row in results
    ]), 200



if __name__ == "__main__":
    app.run(debug=True)



