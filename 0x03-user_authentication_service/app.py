#!/usr/bin/env python3
""" Flask app module
"""
from flask import Flask, jsonify


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/', methods=['GET'], strict_slashes=False)
def greet() -> str:
    """ GET '/'
    Return:
      - JSON body
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.errorhandler(404)
def not_found(error) -> str:
    """ Handle 404 error
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
