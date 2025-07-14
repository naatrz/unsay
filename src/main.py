import requests
import time

# This is the terminal version. To test it, you must manually enter your token (handle this information carefully) and the channel ID.

TOKEN = ""  # Your token
CHANNEL_ID = ""  # Channel ID

headers = {
    "Authorization": TOKEN,
    "User-Agent": "Mozilla/5.0",
}


def get_messages(channel_id, limit=100):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        print(f"Failed to fetch messages: {res.status_code}")
        return []


def delete_message(channel_id, message_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"
    res = requests.delete(url, headers=headers)
    return res.status_code == 204


def delete_own_messages(channel_id):
    user_id = get_user_id()

    if not user_id:
        print("Error getting user ID")
        return

    while True:
        messages = get_messages(channel_id)
        if not messages:
            print("No messages found")
            break

        own_messages = [msg for msg in messages if msg["author"]["id"] == user_id]

        if not own_messages:
            print("No messages sent by you remaining")
            break

        for msg in own_messages:
            success = delete_message(channel_id, msg["id"])
            if success:
                print(f"Message {msg['id']} deleted")
            else:
                print(f"Failed to delete message {msg['id']}")
            time.sleep(1)  # prevent rate limit


def get_user_id():
    res = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    return res.json()["id"]


delete_own_messages(CHANNEL_ID)
