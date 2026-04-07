import requests
import os
from rich.console import Console

from webex_teams import get_team
from webex_space import get_space

# Webex API base URL
BASE_URL = "https://webexapis.com/v1"
# Your Webex access token (replace with your actual token)
ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")
SPACE_NAME = os.getenv("WEBEX_SPACE_NAME")
TEAMS_NAME = os.getenv("WEBEX_TEAMS_NAME")
EMAIL = os.getenv("WEBEX_EMAIL")
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def post_message(space_id, message):
    """Post a message to the space."""
    url = f"{BASE_URL}/messages"
    payload = {
        "roomId": space_id,
        "text": message
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print("Message posted successfully")
    else:
        print(f"Error posting message: {response.text}")

def list_messages(space_id):
    """List messages in the space."""
    url = f"{BASE_URL}/messages"
    data = {"roomId": space_id}
    response = requests.get(url, headers=HEADERS, params=data)
    if response.status_code == 200:
        messages = response.json().get("items", [])
        for msg in messages:
            print(f"Date: {msg['created']}, From: {msg['personEmail']}: {msg['text']}")
    else:
        print(f"Error fetching messages: {response.text}")

def main():
    cli = Console()
    cli.print(f"Posting message to space: {SPACE_NAME}", style="bold green")
    space = get_space()
    space_id = None
    if space:
        for s in space["items"]:
            if s["title"] == SPACE_NAME:
                space_id = s["id"]
                post_message(s["id"], "Hello, this is a message posted via the Webex API!")
                break
    else:
        cli.print(f"Space '{SPACE_NAME}' not found.", style="bold red")

    list_messages(space_id)

if __name__ == "__main__":
    main()