#!/usr/bin/env python3
"""
Flask App for User Authentication Service
"""

from flask import Flask, jsonify
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    """
    Route to return a JSON payload.

    Returns:
        jsonify: JSON response {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """
    Endpoint to register a user.

    Expects form data fields: "email" and "password".
    Responds with JSON payload based on registration success or failure.

    Returns:
        jsonify: JSON response based on registration status.
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = AUTH.register_user(email, password)

        return jsonify({"email": new_user.email, "message": "user
                        created"}), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
