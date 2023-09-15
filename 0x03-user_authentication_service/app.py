#!/usr/bin/env python3
""" Flask app module
"""
from auth import Auth
from flask import abort, Flask, jsonify, request


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def greet() -> str:
    """ GET '/'
    Return:
      - JSON object
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
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
def register_session() -> str:
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


@app.errorhandler(404)
def not_found(error) -> str:
    """ Handle 404 error
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
