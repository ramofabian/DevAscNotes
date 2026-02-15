import requests
import json
from rich.console import Console

cli = Console()
base_url = "https://swapi.info/api/"
endpoints = ["people", "planets", "films", "species", "vehicles", "starships"]

def get_data(endpoint):
    respose = requests.get(base_url + endpoint)
    cli.print(f"ENDPOINT: {endpoint}")
    cli.print(f"Response: {respose}")
    # cli.print(f"Status code: \n{respose.status_code}")
    # cli.print(f"Headers: \n{respose.headers}")
    # cli.print(f"Text: \n{respose.text}")
    data = respose.json()
    cli.print(f"JSON response:")
    cli.print(data[0])
    cli.print("-----------------------------")

for endpoint in endpoints:
    get_data(endpoint)
cli.print("All endpoints have been queried.")
cli.print("#" * 30)
#Challenge: Write a Python script that queries swapi.dev and returns the name field for the Leia Organa character.

cli.print("Challenge: Get Leia Organa's name from the API")
def get_leia_organa():
    response = requests.get(base_url + endpoints[0])
    found_flag = False
    for character in response.json():
        if character.get("name") == "Leia Organa":
             cli.print(f"Found Leia Organa: {character}")
             found_flag = True
             break
    if not found_flag:
        cli.print("Leia Organa not found in the results.")

get_leia_organa()
