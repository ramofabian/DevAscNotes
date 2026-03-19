# Cisco Meraki
- SDN Cloud-managed networking solution for small to medium bussinesses.
- Devices like wireless access points, swtiches and firewalls appliances automatically  download their configuration from the cloud-based Meraki Dashboard. The rapidly enabling deployment with mininal on-site configuration.
- It integrates security with advance firewall capabilities, VPN automation and IoT management, analytics and API integration.
- It uses same concepts from SD-WAN.
- Link: https://meraki.cisco.com/
- Workflow:
    1. Purchase the device
    2. Collect the serial number from the device.
    3. Use serial number to add it on the dashboard on the internet.
    4. Cable the device and turn it on.
    5. Device will do ZTP to get auto-configured ready to use.
- Appliences can be physcal devices or virtual devices:
    - vMX/MX (Secure SD-WAN)

<b>Notes:</b>

- For Meraki we need to generate an API-Key from an exisiting user dashboard and it is allowed to be used only one time.
- In Meraki the word `network` is the site!! not a subnet-IP with vlans.

## Meraki capabilities
1. Network Automation
    - Firewall policies, subnets, vlans, qos
    - Dashboard API
2. Interactive Guest Wi-Fi
    - Captive Portal API:
        - Custome login  to be able use internet (i.e. Airports, hotels internet access).
        - User needs to agree on some terms to be able to use the service.
        - Desing custome landing page or website.
3. Video and Analytics, wayfinding & mapping, Asst Tracking and IoT & Security.
    - IoT services

## Dashboard API
- Link: https://developer.cisco.com/meraki/api-v1/
- Authentication:
    - App-scoped access - Uses OAuth 2.0 grants
    - Admin-scoped access - Uses API keys

- Normal procedure to collect information via API:
    1. Login and get the token
    2. We need to know which is the organization to get the organization ID or orgId.
    3. We need to know which the site name to get the networkId.
    4. We can search and collect information about devices and clients.
- Uses:
    - Configure
    - Monitor
    - in normal cases websocket is not fully need the rest-api. 

### API requests
Requirements:
- Collecting data:
    - `GET` request
    - URL: `https://api.meraki.com/` (URL can change depending on the country)
    - Endpoints:
        - List all organizations: `api/v1/organizations`
        - List all networks inside organizations: `api/v1/organizations/<organization-id>/networks`
        - List all devices inside a network: `api/v1/organizations/<organization-id>/networks/<network-id>/devices`
        - List all clients in an organizations: `api/v1/organizations/{organizationId}/clients/search`
        - List all clients devices in an network: `api/v1/devices/{serial}/clients`
        - List all clients in an network: `api/v1/networks/{networkId}/clients` (We need add timespan and pages values)
    - Headers: 
        - `{'X-Cisco-Meraki-API-key':'<API-Key-Values>'}` (API-Key must be created from meraki portal)
        - `{"Content-Type": "application/json"}`
#### Python script with request library
##### Environment variables
- `MERAKI_API_KEY`: API-Key
- `MERAKI_BASE_URL`: URL (example: ``https://api.meraki.com/``)
- `MERAKI_ORGANIZATION_NAME`: Organization's name
##### Run
From the `Meraki/` folder:
```sh
python merakiDevices.py
```
#### Python script with MerakiSDK libraries
##### Installation
Run the command below:
```sh
pip install meraki
```
##### Environment variables
- `MERAKI_API_KEY`: API-Key
- `MERAKI_ORGANIZATION_NAME`: Organization's name
##### Run
From the `Meraki/` folder:
```sh
python merakiDevicesSdk.py
```
