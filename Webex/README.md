# Webex
- Conferents calls system.
- Jabber (legacy product)
    - Chat system
    - It can communicate with CUCM and then have calls to phones.
- Cisco convergeed both products in into one called **Webex Teams** and more products were added.
- Link: 
    - https://www.webex.com/
    - https://developer.webex.com/

## Webex app
- Chats are called space
- Teams are the groups
- Usually the space contains a set of teams

- Link to get the access tocken: [Documentation](https://developer.webex.com/docs/getting-your-personal-access-token), this token expires in 12hrs.

## Working with WebEx API
- API docuemntation:
    - https://developer.webex.com/calling/docs/getting-started
    - https://developer.webex.com/messaging/docs/getting-started
- Endpoints:
    - Manage a teams: `{BASE_URL}/teams`
    - Manage a spaces: `{BASE_URL}/rooms`
    - Manage a people to spaces: `{BASE_URL}/memberships`
    - Manage a people to team: `{BASE_URL}/team/memberships`
    - Post messages: `{BASE_URL}/messages`

### Python scripts
Needed virtual env vars:
```sh
WEBEX_TEAMS_NAME=<NEW-TEAMS-NAME>
WEBEX_SPACE_NAME=<NEW_NAMESPCE-NAME>
WEBEX_EMAIL=<NEW-USER-TO-BE-ADDED-IN_ROOM>
WEBEX_ACCESS_TOKEN=<WEBEX-TOKEN-FROM-WEB-PORTAL>
```
- Create a teams: `webex_teams.py`
- Create a teams: `webex_space.py`
- Add a user to teams: `webex_users.py`
- Post a message and list all of them: `webex_post_msg.py`
