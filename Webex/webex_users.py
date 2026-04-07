import requests, os
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

def add_member_to_space(space_id, email):
    """Add a member to the space."""
    url = f"{BASE_URL}/memberships"
    payload = {
        "roomId": space_id,
        "personEmail": email,
        "isModerator": False
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print(f"Successfully added {email} to the space")
    else:
        print(f"Error adding member: {response.text}")

def add_member_to_team(team_id, email):
    """Add a member to the team."""
    url = f"{BASE_URL}/team/memberships"
    payload = {
        "teamId": team_id,
        "personEmail": email,
        "isModerator": False
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print(f"Successfully added {email} to the team")
    else:
        print(f"Error adding member to team: {response.text}")

def get_team_members(team_id):
    """Get members of a team."""
    url = f"{BASE_URL}/team/memberships?teamId={team_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"Error fetching team members: {response.text}")
        return []

def get_space_members(space_id):
    """Get members of a space."""
    url = f"{BASE_URL}/memberships?roomId={space_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"Error fetching space members: {response.text}")
        return []

def main():
    cli = Console()
    cli.print(f"Adding {EMAIL} to space: {SPACE_NAME} and team: {TEAMS_NAME}", style="bold green")
    space = get_space()
    space_id = ""
    if space:
        for s in space["items"]:
            if s["title"] == SPACE_NAME:
                space_id = s["id"]
                add_member_to_space(space_id, EMAIL)
                break
    else:
        cli.print(f"Space '{SPACE_NAME}' not found.", style="bold red")

    team = get_team()
    team_id = ""
    if team:
        for team in team["items"]:
            if team["name"] == TEAMS_NAME:
                team_id = team["id"]
                add_member_to_team(team["id"], EMAIL)
                break
    else:
        cli.print(f"Team '{TEAMS_NAME}' not found.", style="bold red")
    #################################################################

    cli.print(f"Members of space '{SPACE_NAME}':", style="bold blue")
    space_members = get_space_members(space_id)
    for member in space_members:
        cli.print(f" - {member['personEmail']}", style="bold cyan")

    cli.print(f"Members of team '{TEAMS_NAME}':", style="bold blue")
    team_members = get_team_members(team_id)
    for member in team_members:
        cli.print(f" - {member['personEmail']}", style="bold cyan")

    cli.print("Done!", style="bold green")

if __name__ == "__main__":    
    main()
