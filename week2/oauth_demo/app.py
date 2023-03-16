from datetime import datetime, timedelta, timezone
from pprint import pprint
import secrets
from functools import wraps

import requests
from flask import Flask, abort, g, redirect, render_template, request, session, url_for
import urllib.parse

CLIENT_ID = "1078198017678647307"
CLIENT_SECRET = "QfaLfJv1nmTZS8qjO6f09c-REllTM8x4"
AUTHORIZE_URL = "https://discord.com/oauth2/authorize"
TOKEN_URL = "https://discord.com/api/oauth2/token"
PROFILE_URL = "https://discord.com/api/v10/users/@me"
SCOPES = "identify"
REDIRECT_URI = "http://127.0.0.1:5000/callback"

r = requests.session()
r.proxies = {"https": "http://127.0.0.1:8080"}
r.verify = False

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(64)


@app.before_request
def before_request():
    now = datetime.now(tz=timezone.utc)
    access_token = session.get("access_token")
    expires_at = session.get("expires_at")
    if access_token is None or expires_at is None:
        g.logged_in = False
    else:
        g.logged_in = now < expires_at - timedelta(seconds=30)


def auth_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        if g.logged_in:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return _wrapper


def noauth_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        if not g.logged_in:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("index"))

    return _wrapper


@app.route("/")
@auth_required
def index():
    profile = r.get(
        PROFILE_URL, headers={"Authorization": f"Bearer {session['access_token']}"}
    ).json()

    pprint(profile)
    return render_template("index.html", profile=profile)


@app.route("/login")
@noauth_required
def login():
    return render_template("login.html")


@app.route("/discord-auth")
def discord_auth():
    session["state"] = secrets.token_urlsafe(32)
    return redirect(
        f"{AUTHORIZE_URL}?"
        + urllib.parse.urlencode(
            {
                "response_type": "code",
                "client_id": CLIENT_ID,
                "scope": SCOPES,
                "state": session["state"],
                "redirect_uri": REDIRECT_URI,
                "prompt": "consent",
            }
        )
    )


@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")
    if code is None or state is None:
        abort(400)

    if session.get("state") != state:
        abort(400)

    res = r.post(
        TOKEN_URL,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
    )
    res.raise_for_status()
    data = res.json()

    session["access_token"] = data["access_token"]
    session["refresh_token"] = data["refresh_token"]
    session["expires_at"] = datetime.now() + timedelta(seconds=data["expires_in"])

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
