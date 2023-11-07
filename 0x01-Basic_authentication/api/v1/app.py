#!/usr/bin/env python3

"""
Flask app with error handler for 401 status code.
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.errorhandler(401)
def unauthorized_error(error):
    """
    Handle 401 error.
    """
    return jsonify({'error': 'Unauthorized'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
