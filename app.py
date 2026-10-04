import os
from urllib.parse import urlencode
import requests
from flask import Flask, redirect, request, render_template

app = Flask(__name__)

GUMROAD_AUTHORIZE_URL = "https://gumroad.com/oauth/authorize"
GUMROAD_TOKEN_URL = "https://api.gumroad.com/v2/oauth/token"

@app.get("/")
def home():
    client_id = os.getenv("GUMROAD_CLIENT_ID", "")
    redirect_uri = os.getenv("GUMROAD_REDIRECT_URI", "")
    if not client_id or not redirect_uri:
        return render_template("index.html", configured=False, redirect_uri=redirect_uri)
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
    }
    return render_template("index.html", configured=True,
                           authorize_url=GUMROAD_AUTHORIZE_URL + "?" + urlencode(params),
                           redirect_uri=redirect_uri)

@app.get("/auth/gumroad/callback")
def callback():
    error = request.args.get("error")
    if error:
        return render_template("result.html", ok=False, message=f"Gumroad authorization failed: {error}")

    code = request.args.get("code")
    if not code:
        return render_template("result.html", ok=False, message="No authorization code was returned by Gumroad.")

    data = {
        "client_id": os.getenv("GUMROAD_CLIENT_ID", ""),
        "client_secret": os.getenv("GUMROAD_CLIENT_SECRET", ""),
        "redirect_uri": os.getenv("GUMROAD_REDIRECT_URI", ""),
        "code": code,
        "grant_type": "authorization_code",
    }
    try:
        response = requests.post(GUMROAD_TOKEN_URL, data=data, timeout=20)
        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            return render_template("result.html", ok=False,
                                   message="Gumroad responded successfully, but no access token was returned.")
        # Do not display or log the token. Store it securely in your real integration.
        return render_template("result.html", ok=True,
                               message="Gumroad connected successfully. Your OAuth flow is working.",
                               note="The access token is intentionally not displayed.")
    except requests.RequestException as exc:
        return render_template("result.html", ok=False,
                               message=f"Token exchange failed: {exc}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "3000")))
