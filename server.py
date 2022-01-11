import os
import json
import datetime
import base64
import flask
import flask_session
import google.auth.transport.requests
import google_auth_oauthlib.flow
import google.oauth2.id_token
import monitor
from doorlock_config import config, get_file, refresh_config, update_config


# App constants
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]
client_secrets_file = get_file("client_secret.json")
app = flask.Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_USE_SIGNER"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = \
    datetime.timedelta(days=config['sessionLifetime'])
flask_session.Session(app)

# Get Google client ID
with open(client_secrets_file, "r") as client_secrets:
    google_client_id = json.load(client_secrets)["web"]["client_id"]

# Get app.secret_key (create one if it does not exist yet)
if 'sessionSignKey' not in config or len(config['sessionSignKey']) < 1:
    config['sessionSignKey'] = base64.b64encode(os.urandom(64)).decode('utf-8')
    update_config(config)
app.secret_key = config['sessionSignKey']


def auth_required(function):
    def wrapper(*args, **kwargs):
        if "email" not in flask.session:
            return flask.redirect("/login")
        elif flask.session["email"] not in config['authorizedEmails']:
            flask.session.clear()
            return flask.abort(401)
        else:
            return function()
    wrapper.__name__ = function.__name__
    return wrapper


@app.route("/login")
def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    flow.redirect_uri = flask.url_for("login_callback", _external=True)
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true")
    flask.session["state"] = state
    return flask.redirect(authorization_url)


@app.route("/login-callback")
def login_callback():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file, SCOPES, state=flask.session["state"])
    flow.redirect_uri = flask.url_for("login_callback", _external=True)
    flow.fetch_token(authorization_response=flask.request.url)

    if flask.session["state"] != flask.request.args["state"]:
        return flask.abort(500)

    id_info = google.oauth2.id_token.verify_oauth2_token(
        id_token=flow.credentials._id_token,
        request=google.auth.transport.requests.Request(),
        audience=google_client_id,
    )

    flask.session["name"] = id_info.get("name")
    if id_info.get("email_verified"):
        flask.session["email"] = id_info.get("email")
    return flask.redirect("/")


@app.route("/")
@auth_required
def index():
    return f"""Hello {flask.session["name"]}! Here are your options:
<br>
<form>
  <button formaction="/lock">Lock door</button>
  <button formaction="/unlock">Unlock door</button>
</form>
"""


@app.route("/unlock")
@auth_required
def unlock():
    monitor.unlock()
    return "Door unlocked!"


@app.route("/lock")
@auth_required
def lock():
    monitor.lock()
    return "Door locked!"


@app.route("/refresh-authorized-emails")
def refresh_authorized_emails():
    refresh_config()
    return "Refreshed the authorized email list"


# Run the app at localhost:8080
if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run("localhost", 8080, debug=True)
