#!/usr/bin/env python3
""" Module of Session Authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user() -> str:
    """ POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 40x if can't create the new User
    """
    rj = None
    error_msg = None

    try:
        rj = request.form
    except Exception as e:
        rj = None
        error_msg = "email missing"
    finally:
        if error_msg is None and rj.get("email", "") == "":
            error_msg = "email missing"
        if error_msg is None and rj.get("password", "") == "":
            error_msg = "password missing"
        if error_msg is not None:
            return jsonify({'error': error_msg}), 400

    if error_msg is None:
        email = request.form.get('email')
        password = request.form.get('password')
        user_list = User.search({'email': email})

        if user_list:
            user = user_list[0]
            if not user.is_valid_password(password):
                error_msg = "wrong password"
                return jsonify({'error': error_msg}), 401
            else:
                from api.v1.app import auth
                SESSION_NAME = getenv('SESSION_NAME')

                session_id = auth.create_session(user.id)
                response = jsonify(user.to_json())
                print(type(response))
                response.set_cookie(SESSION_NAME, session_id)
                return response
        else:
            error_msg = "no user found for this email"
            return jsonify({'error': error_msg}), 404


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout_user() -> str:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - empty JSON if the user session has been correctly destroyed
      - 404 if the User ID and/or Session ID are null
    """
    from api.v1.app import auth

    result = auth.destroy_session(request)
    if not result:
        abort(404)
    return jsonify({}), 200
