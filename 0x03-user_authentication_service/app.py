#!/usr/bin/env python3
"""
Flask App for User Authentication Service
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def welcome():
    """
    Route to return a JSON payload.

    Returns:
        jsonify: JSON response {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
