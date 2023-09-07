#!/usr/bin/env python3
""" Module of Session Authentication views
"""
from api.v1.views import app_views
from flask import jsonify, request
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
                response.set_cookie(SESSION_NAME, session_id)
                return response
        else:
            error_msg = "no user found for this email"
            return jsonify({'error': error_msg}), 404



"""
You must use request.form.get() to retrieve email and password parameters
If email is missing or empty, return the JSON { "error": "email missing" } with the status code 400
If password is missing or empty, return the JSON { "error": "password missing" } with the status code 400
Retrieve the User instance based on the email - you must use the class method search of User (same as the one used for the BasicAuth)
If no User found, return the JSON { "error": "no user found for this email" } with the status code 404
If the password is not the one of the User found, return the JSON { "error": "wrong password" } with the status code 401 - you must use is_valid_password from the User instance
Otherwise, create a Session ID for the User ID:
You must use from api.v1.app import auth - WARNING: please import it only where you need it - not on top of the file (can generate circular import - and break first tasks of this project)
You must use auth.create_session(..) for creating a Session ID
Return the dictionary representation of the User - you must use to_json() method from User
You must set the cookie to the response - you must use the value of the environment variable SESSION_NAME as cookie name - tip
"""
