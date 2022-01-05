import os
import pathlib
import flask
import google_auth_oauthlib.flow

client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")
# TODO check these scopes
scopes = ["https://www.googleapis.com/auth/userinfo.profile",
          "https://www.googleapis.com/auth/userinfo.email", "openid"]

app = flask.Flask("doorlock")
# FIXME: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
# Probably just get some bytes from random and save to a file
# if secret_key file DNE:
#   create secret_key file from 128 random bytes
# read app.secret_key from secret_key file
app.secret_key = "REPLACE ME - this value is here as a placeholder."

# SEE https://developers.google.com/identity/protocols/oauth2/web-server#python
# SEE https://flasksession.readthedocs.io/en/latest/


def login_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in flask.session:
            return flask.redirect("/login")
        elif False:  # TODO not authorized
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

    flask.session["google_id"] = id_info.get("sub")
    flask.session["name"] = id_info.get("name")
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
    # TODO unlock the door using GPIO
    return "Door unlocked!"


@app.route("/lock")
@login_required
def lock():
    # TODO lock the door using GPIO
    return "Door locked!"


# Run the app at localhost:8080
if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run("localhost", 8080, debug=True)
