#!/usr/bin/env python3
""" test module """
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://127.0.0.1:5000/"


def register_user(email: str, password: str) -> None:
    """tests user registration"""
    info = {"email": email, "password": password}
    endpoint = BASE_URL + "users"
    res = requests.post(endpoint, data=info)
    assert 200 == res.status_code
    assert {"email": email, "message": "user created"} == res.json()


def profile_unlogged() -> None:
    """test getting user info"""
    endpoint = BASE_URL + "profile"

    cookie = {"session_id": "wrong cookie"}
    res = requests.get(endpoint, cookies=cookie)
    assert 403 == res.status_code


def log_in(email: str, password: str) -> str:
    """test loggin in"""
    # get session_id
    endpoint = BASE_URL + "sessions"
    info = {"email": email, "password": password}
    res = requests.post(endpoint, info)
    cookie = res.cookies["session_id"]
    assert 200 == res.status_code
    assert isinstance(cookie, str)
    return cookie


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """tests updating passwd"""
    endpoint = BASE_URL + "reset_password"
    info = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    res = requests.put(endpoint, data=info)
    assert 200 == res.status_code
    payload = res.json()
    assert payload == {"email": email, "message": "Password updated"}


def profile_logged(session_id: str) -> None:
    """test user info logging in"""
    endpoint = BASE_URL + "profile"
    cookie = {"session_id": session_id}
    res = requests.get(endpoint, cookies=cookie)
    assert 200 == res.status_code
    assert {"email": EMAIL} == res.json()


def log_in_wrong_password(email: str, password: str) -> None:
    """tests logging in with wrong password"""
    endpoint = BASE_URL + "sessions"
    info = {"email": email, "password": "wrong pswd"}
    res = requests.post(endpoint, data=info)
    assert 401 == res.status_code


def log_out(session_id: str) -> None:
    """test logging out"""
    endpoint = BASE_URL + "sessions"
    cookie = {"session_id": session_id}
    res = requests.delete(endpoint, cookies=cookie)
    assert 200 == res.status_code


def reset_password_token(email: str) -> str:
    """test  passwd reset"""
    endpoint = BASE_URL + "reset_password"
    info = {
        "email": email,
    }
    res = requests.post(endpoint, data=info)
    assert 200 == res.status_code
    token = res.json()["reset_token"]
    assert len(token) == 36
    return token


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
