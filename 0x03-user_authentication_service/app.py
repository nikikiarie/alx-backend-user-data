#!/usr/bin/env python3
"""A simple Flask app
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect, Response


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index() -> Response:
    """Index page
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """Handles Registration
    """
    mail, passwd = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(mail, passwd)
        return jsonify({"email": mail, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
