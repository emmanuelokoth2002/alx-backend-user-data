#!/usr/bin/env python3
from flask import request, jsonify, abort
from api.v1.views import app_views
from api.v1.auth import auth
from models.user import User


@app_views.route('/auth_session/login', methods=['POST', 'GET'],
                 strict_slashes=False)
    def auth_session_login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            if email is None or email == "":
                return jsonify({"error": "email missing"}), 400

            if password is None or password == "":
                return jsonify({"error": "password missing"}), 400

            user = User.search({'email': email})
            if not user:
                return jsonify({"error": "no user found for this email"}), 404

            if not user[0].is_valid_password(password):
                return jsonify({"error": "wrong password"}), 401

            session_id = auth.create_session(user[0].id)
            response = user[0].to_json()
            response["session_id"] = session_id

            return jsonify(response), 200
        else:
            abort(405)
@session_auth_bp.route('/logout', methods=['DELETE'])
    def logout():
        if not auth.destroy_session(request):
            abort(404)

        return jsonify({})
