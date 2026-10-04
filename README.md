# Gumroad OAuth Connector

A minimal Flask app for Gumroad OAuth.

## Gumroad settings

Create the application in Gumroad Settings -> Advanced. Gumroad says the Advanced settings are where API applications are created.

Set the Redirect URI to the exact public URL of this app:

`https://YOUR-DOMAIN/auth/gumroad/callback`

Do not use a random URL. The deployed app must have the `/auth/gumroad/callback` route.

## Environment variables

Set:
- GUMROAD_CLIENT_ID
- GUMROAD_CLIENT_SECRET
- GUMROAD_REDIRECT_URI

Then run:

`pip install -r requirements.txt`
`python app.py`

For local testing, the redirect URI can be:
`http://localhost:3000/auth/gumroad/callback`

For production, use HTTPS and keep the client secret server-side.
