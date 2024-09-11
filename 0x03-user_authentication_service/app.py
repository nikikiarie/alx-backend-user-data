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


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """Login function
    """
    email, passwd = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, passwd):
        abort(401)
    id_session = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", id_session)
    return res


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ handles session deletion """
    id_session = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(id_session)
    if not user:
        abort(403)

    AUTH.destroy_session(id_session)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
