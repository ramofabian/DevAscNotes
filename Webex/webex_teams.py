
import requests
import os
from rich.console import Console
from rich.table import Table

# Webex API base URL
BASE_URL = "https://webexapis.com/v1"
# Your Webex access token (replace with your actual token)
ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")
TEAM_ID = os.getenv("WEBEX_TEAM_ID")
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def create_team(team_name):
    """Create a new Webex team."""
    url = f"{BASE_URL}/teams"
    payload = {
        "name": team_name,
        "description": "This is a team created via the Webex API wirtten in Python."
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    # response.raise_for_status()  # Raise an exception for HTTP errors
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Error creating team: {response.text}")
        return None
    
def get_team():
    """Get information about a specific Webex team."""
    url = f"{BASE_URL}/teams"
    payload = {}
    
    response = requests.get(url, headers=HEADERS, json=payload)
    # response.raise_for_status()  # Raise an exception for HTTP errors
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting team: {response.text}")
        return None
    
def delete_team(team_id):
    """Delete a specific Webex team."""
    url = f"{BASE_URL}/teams/{team_id}"
    payload = {}
    
    response = requests.delete(url, headers=HEADERS, json=payload)
    # response.raise_for_status()  # Raise an exception for HTTP errors
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error deleting team: {response.text}")
        return None
    
def main():
    cli = Console()
    team_name = "My_new_team"
    team_id = create_team(team_name)
    if team_id:
        cli.print(f"Team created successfully with ID: {team_id}")
    else:
        cli.print("Failed to create team.")

    ############################################

    team_info = delete_team(TEAM_ID)
    if team_info:
        cli.print(f"Team deleted successfully with ID: {TEAM_ID}")
    else:
        cli.print("Failed to delete team.")

    ############################################
    cli.print("Getting team information...")
    team_info = get_team()
    table_pf = Table(title="Webex Teams Information")
    table_pf.add_column("ID", style="cyan", no_wrap=True)
    table_pf.add_column("Name", style="magenta")
    table_pf.add_column("Description", style="green")
    table_pf.add_column("Created", style="yellow")
    if team_info:
        print("Team information retrieved successfully:")
        for team in team_info["items"]:
            table_pf.add_row(
                team["id"], team["name"],
                team["description"] if "description" in team.keys() else "N/A", team["created"]
            )
        cli.print(table_pf)    
    else:
        cli.print("Failed to retrieve team information.")

if __name__ == "__main__":
    main()