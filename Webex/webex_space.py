import requests, os
from rich.console import Console

from webex_teams import get_team

# Webex API base URL
BASE_URL = "https://webexapis.com/v1"
# Your Webex access token (replace with your actual token)
ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")
SPACE_NAME = os.getenv("WEBEX_SPACE_NAME")
TEAMS_NAME = os.getenv("WEBEX_TEAMS_NAME")
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def create_space(team_id, space_name):
    """Create a new space in the team."""
    url = f"{BASE_URL}/rooms"
    payload = {
        "title": space_name,
        "teamId": team_id
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Error creating space: {response.text}")
        return None

def get_space(team_id='all'):
    """Get information about a specific space."""
    if team_id != 'all':
        url = f"{BASE_URL}/rooms?teamId={team_id}"
    else:
        url = f"{BASE_URL}/rooms"
    payload = { }
    
    response = requests.get(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting space: {response.text}")
        return None
    
def delete_space(space_id):
    """Delete a specific space."""
    url = f"{BASE_URL}/rooms/{space_id}"
    payload = {}
    
    response = requests.delete(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error deleting space: {response.text}")
        return None

def main():
    cli = Console()
    team_info = get_team()
    team_id = ""
    for team in team_info["items"]:
        if team["name"] == TEAMS_NAME:
            team_id = team["id"]
            break
    cli.print(f"Team ID for '{TEAMS_NAME}': {team_id}")

    cli.print("Getting space information...")
    space_info = get_space(team_id)
    cli.print(f"Space information for team '{TEAMS_NAME}':\n", space_info)

    if team_id:
        space_id = create_space(team_id, SPACE_NAME)
        if space_id:
            cli.print(f"Space created successfully with ID: {space_id}")
        else:
            cli.print("Failed to create space.")

    cli.print("Getting space information...")
    space_info = get_space(team_id)
    cli.print(f"Space information for team '{TEAMS_NAME}':\n", space_info)

if __name__ == "__main__":    
    main()