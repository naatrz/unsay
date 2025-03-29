from fastapi import FastAPI
import requests

app = FastAPI()
DISCORD_API = "https://discord.com/api/v9"
TOKEN = "SEU_TOKEN_AQUI"


@app.get("/messages/{channel_id}")
def get_messages(channel_id: str):
    headers = {"Authorization": f"Bot {TOKEN}"}
    response = requests.get(
        f"{DISCORD_API}/channels/{channel_id}/messages?limit=50", headers=headers
    )

    if response.status_code != 200:
        return {"error": "Falha ao buscar mensagens", "status": response.status_code}

    return response.json()
