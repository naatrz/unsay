from fastapi import FastAPI, Request
import uvicorn
import requests
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


@app.get("/auth/callback")
def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code provided"}

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(
        "https://discord.com/api/oauth2/token", data=data, headers=headers
    )
    if response.status_code != 200:
        return {"error": "Failed to get access token", "details": response.text}

    access_token = response.json()["access_token"]

    user_info = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    return user_info.json()
