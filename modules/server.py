import os
import json
from flask import Flask, session, request, redirect, abort, url_for
from flask_session import Session
from google.oauth2.id_token import verify_oauth2_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import modules.controller as controller
from config.doorlock import get_config_file, session_lifetime, session_sign_key, authorized_emails


# App constants
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]
client_secrets_file = get_config_file("client_secret.json")
app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_USE_SIGNER"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = session_lifetime
app.secret_key = session_sign_key
Session(app)

# Get Google client ID
with open(client_secrets_file, "r") as client_secrets:
    google_client_id = json.load(client_secrets)["web"]["client_id"]


def auth_required(function):
    def wrapper(*args, **kwargs):
        if "email" not in session:
            return redirect("/login")
        elif session["email"] not in authorized_emails:
            session.clear()
            return abort(401)
        else:
            return function()
    wrapper.__name__ = function.__name__
    return wrapper


@app.route("/login")
def login():
    flow = Flow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    flow.redirect_uri = url_for("login_callback", _external=True)
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true")
    session["state"] = state
    return redirect(authorization_url)


@app.route("/login-callback")
def login_callback():
    flow = Flow.from_client_secrets_file(
        client_secrets_file, SCOPES, state=session["state"])
    flow.redirect_uri = url_for("login_callback", _external=True)
    flow.fetch_token(authorization_response=request.url)

    if session["state"] != request.args["state"]:
        return abort(500)

    id_info = verify_oauth2_token(
        id_token=flow.credentials._id_token,
        request=Request(),
        audience=google_client_id,
    )

    session["name"] = id_info.get("name")
    if id_info.get("email_verified"):
        session["email"] = id_info.get("email")
    return redirect("/")


@app.route("/")
@auth_required
def index():
    return f"""Hello {session["name"]}! Here are your options:
<br>
<form>
  <button formaction="/lock">Lock door</button>
  <button formaction="/unlock">Unlock door</button>
</form>
"""


@app.route("/unlock")
@auth_required
def unlock():
    controller.unlock()
    return "Door unlocked!"


@app.route("/lock")
@auth_required
def lock():
    controller.lock()
    return "Door locked!"


# Run the app at localhost:8080
if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run("localhost", 8080, debug=True)
