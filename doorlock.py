import os
import pathlib
import flask
import string
import random
import google_auth_oauthlib.flow
import servo_control


def get_file(filename):
    return os.path.join(pathlib.Path(__file__).parent, filename)


# App constants
app_secret_key_file = get_file("app_secret_key.txt")
client_secrets_file = get_file("client_secret.json")
scopes = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]
app = flask.Flask("doorlock")

# Configure authorized_emails
authorized_emails = set()
with open(get_file("authorized_emails.txt"), "r") as ids:
    for id in ids:
        authorized_emails.add(id.rstrip())
if '' in authorized_emails:
    authorized_emails.remove('')

# Configure app.secret_key (create one if it does not exist yet)
if not os.path.exists(app_secret_key_file):
    with open(app_secret_key_file, "w") as file:
        chars = string.ascii_letters + string.digits
        file.write("".join(random.choice(chars) for i in range(128)))
with open(app_secret_key_file, "r") as file:
    app.secret_key = file.read().rstrip()


# TODO
# SEE https://developers.google.com/identity/protocols/oauth2/web-server#python
# SEE https://flasksession.readthedocs.io/en/latest/


def login_required(function):
    def wrapper(*args, **kwargs):
        if "email" not in flask.session:
            return flask.redirect("/login")
        elif flask.session["email"] not in authorized_emails:
            flask.session.clear()
            return flask.abort(401)
        else:
            return function()
    return wrapper


@app.route("/login")
def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file, scopes)
    flow.redirect_uri = flask.url_for("login_callback", _external=True)
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true")
    flask.session["state"] = state
    return flask.redirect(authorization_url)


@app.route("/logout")
def logout():
    flask.session.clear()
    return flask.redirect("/")


@app.route("/login-callback")
def login_callback():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file, scopes, state=flask.session["state"])
    flow.redirect_uri = flask.url_for("login_callback", _external=True)
    flow.fetch_token(authorization_response=flask.request.url)

    # TODO check the following
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    flask.session["name"] = id_info.get("name")
    flask.session["email"] = id_info.get("email")
    return flask.redirect("/")


@app.route("/")
@login_required
def index():
    return f"""Hello {flask.session["name"]}! Here are your options:
<br>
<form>
  <button formaction="/lock">Lock door</button>
  <button formaction="/unlock">Unlock door</button>
  <button formaction="/logout">Logout</button>
</form>
"""


@app.route("/unlock")
@login_required
def unlock():
    servo_control.unlock()
    return "Door unlocked!"


@app.route("/lock")
@login_required
def lock():
    servo_control.lock()
    return "Door locked!"


# Run the app at localhost:8080
if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run("localhost", 8080, debug=True)
