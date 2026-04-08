# Webex
- Conference calling system.
- Jabber (legacy product)
    - Chat system
    - It can communicate with CUCM and then have calls to phones.
- Cisco converged both products into one called **Webex Teams** and more products were added.
- Link: 
    - https://www.webex.com/
    - https://developer.webex.com/

## Webex app
- Chats are called spaces.
- Teams are the groups
- Usually the space contains a set of teams

- Link to get the access token: [Documentation](https://developer.webex.com/docs/getting-your-personal-access-token), this token expires in 12hrs.

## Working with WebEx API
- API documentation:
    - https://developer.webex.com/calling/docs/getting-started
    - https://developer.webex.com/messaging/docs/getting-started
- Endpoints:
    - Manage teams: `{BASE_URL}/teams`
    - Manage spaces: `{BASE_URL}/rooms`
    - Manage people to spaces: `{BASE_URL}/memberships`
    - Manage people to team: `{BASE_URL}/team/memberships`
    - Post messages: `{BASE_URL}/messages`

### Python scripts
Needed virtual environment variables:
```sh
WEBEX_TEAMS_NAME=<NEW-TEAMS-NAME>
WEBEX_SPACE_NAME=<NEW-NAMESPCE-NAME>
WEBEX_EMAIL=<NEW-USER-TO-BE-ADDED-IN_ROOM>
WEBEX_ACCESS_TOKEN=<WEBEX-TOKEN-FROM-WEB-PORTAL>
```
- Create a teams: `webex_teams.py`
- Create an Space: `webex_space.py`
- Add a user to teams: `webex_users.py`
- Post a message and list all of them: `webex_post_msg.py`
