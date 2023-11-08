#!/usr/bin/env python3

"""
Endpoints for the Flask app.
"""

from flask import Blueprint, abort

index = Blueprint('index', __name__)


@index.route('/api/v1/unauthorized', methods=['GET'])
def unauthorized_endpoint():
    """
    Endpoint to raise a 401 error.
    """
    abort(401)
