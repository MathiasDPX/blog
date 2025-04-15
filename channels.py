"""
Create a dict of channel_id: channel_name for scrapbook
"""

from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

ACCESS_TOKEN = os.getenv("CHANNEL_LIST_TOKEN")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

params = {
    "types": "public_channel",
    "limit": 1000
}

channels_map = {}

while True:
    response = requests.get("https://slack.com/api/conversations.list", headers=headers, params=params)
    data = response.json()

    if not data.get("ok"):
        print("Error:", data.get("error"))
        break

    for channel in data.get("channels", []):
        channels_map[channel["id"]] = channel["name"]

    cursor = data.get("response_metadata", {}).get("next_cursor")
    if cursor:
        params["cursor"] = cursor
    else:
        break

print(f"{len(channels_map)} public channels found")

with open("channels.json", "w+") as f:
    json.dump(channels_map, f)