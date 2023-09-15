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
      - JSON object
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def register() -> str:
    """ POST '/users'
    JSON body:
      - email
      - password
    Return:
      - User JSON object
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
      - User JSON object with login status
    """
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    if not email or not password:
        abort(401, description="Invalid request data")

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


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Log out a logged in user and destroy their session
    """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None or session_id is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    Return a user's email based on session_id in the received cookies
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Generate a token for resetting a user's password
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": f"{email}", "reset_token": f"{reset_token}"})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    Update a user's password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": f"{email}", "message": "Password updated"})


@app.errorhandler(404)
def not_found(error) -> str:
    """ Handle 404 error
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
