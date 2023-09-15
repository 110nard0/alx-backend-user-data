#!/usr/bin/env python3
""" Flask app module
"""
from auth import Auth
from flask import abort, Flask, jsonify, request


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET '/'
    Return:
      - JSON string
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ GET '/profile'
    Request body:
      - session_id
    Return:
      - User JSON object with email field
    """
    session_cookie = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_cookie)
    if session_cookie is None or user is None:
        abort(403, description="Invalid user")
    return jsonify({"email": user.email})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register() -> str:
    """ POST '/users'
    JSON body:
      - email
      - password
    Return:
      - User JSON object with email and status message
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({
                        "email": user.email,
                        "message": "user created"
                       })
    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST '/sessions'
    JSON body:
      - email
      - password
    Return:
      - User JSON object with email and login status
    """
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    if not email or not password:
        abort(401, description="Invalid request form data")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({
                            "email": email,
                            "message": "logged in"
                           })
        response.set_cookie("session_id", session_id)
        return response, 200
    else:
        abort(401, description="Invalid username or password")


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> None:
    """ DELETE '/sessions'
    Request body:
      - session_id
    """
    session_cookie = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_cookie)
    if session_cookie is None or user is None:
        abort(403, description="Invalid user")
    AUTH.destroy_session(user.id)
    return redirect('/', 302)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_token() -> str:
    """ POST '/reset_password'
    Request body:
      - email
    Return:
      - User JSON object with email and reset_token fields
    """
    email = request.form.get('email', '')
    if not email:
        abort(401, description="Invalid credentials")

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403, description="User not registered")
    else:
        return jsonify({
                        "email": email,
                        "reset_token": reset_token
                       }), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ PUT '/reset_password'
    Request body:
      - email
      - reset_token
      - new_password
    Return:
      - User JSON object with email and status message
    """
    email = request.form.get('email', '')
    reset_token = request.form.get('reset_password', '')
    new_password = request.form.get('new_password', '')
    if not email or not reset_token or not new_password:
        abort(401, description="Invalid request form data")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403, description="User not registered")
    else:
        return jsonify({
                        "email": email,
                        "message": "Password updated"
                       }), 200


@app.errorhandler(404)
def not_found(error) -> str:
    """ Handle 404 error
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
