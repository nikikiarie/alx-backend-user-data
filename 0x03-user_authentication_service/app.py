#!/usr/bin/env python3
"""A simple Flask app
"""
from auth import Auth
from flask import Flask, jsonify, url_for, request, abort, redirect, Response


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
    """ handles session delete"""
    id_session = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(id_session)
    if not user:
        abort(403)
    AUTH.destroy_session(id_session)
    return redirect(url_for('index'))


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """ /profile route
    """
    id_session = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(id_session)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ token to reset passwd"""
    email = request.form.get('email')
    try:
        auth_token = AUTH.get_reset_password_token(email)
    except Exception:
        abort(403)
    return jsonify({
        'email': email, 'reset_token': auth_token
    })


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ updates user passwd """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    passwd_new = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, passwd_new)
    except Exception:
        abort(403)
    return jsonify({
        'email': email, 'message': 'Password updated'
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
