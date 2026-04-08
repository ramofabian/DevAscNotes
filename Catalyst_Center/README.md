# Automate with Catalyst Center and DNA
- SDN controller
- It is used for Catalyst 9000
- Attach policies on a predefined place, this policy contains parameter which will change if the same application is moved to another location.
- It uses LISP (location ID) + VXLAN + IS-IS

## 5 Applications
1. Design: Global layout, name address.
2. Policy: Group based access control and IP and URL Based Access Control
3. Provision: Inventory (discovery), Software defined Access layer, Wireless.
4. Assurance: Health and analytics
5. Platform: System API
    - North-south API
        - Northbound API - Client computer/server
        - Southbound there is Infra
    - East API -> EVENT -> Outgoing external Applications (webhooks)
    - West API Input external Applications -> Applications where Catalyst Center relies on.
        - Cisco ISE (AAA)
        - DHCP (IPAM)
        - DNS
    - Path: Platform/Developer toolkit (API DOC/Swagger documentation)
## Working Catalyst Center using Postman and Python 
- Endpoint definition:
    ```sh
      https://{{DNA_IP}}/dna/system/api/v1/auth/token
              |_________|_________________|__________|
                  |            |               |->Sub module section
                  |            |->Main module section: system, intent, etc..
                  |-> FQDN/IP
    ```
### Postman
1. Create DNA collection and environment.
2. Create environment variables:
    - `DNA_IP`
    - `DNA_USER`
    - `DNA_PASSWORD` (enable encryption)
    - `DNA_TOKEN` (enable encryption)
3. Make sure the created environment is created.
4. Requests:
    - Login: `https://{{DNA_IP}}/dna/system/api/v1/auth/token`
        - `POST` request
        - Enable basic authentication and add user and password
        - JavaScript to extract the token from body response into `DNA_TOKEN`
        ```js
        var jsonData = pm.response.json();
        var tk = jsonData.Token;
        pm.environment.set("DNA_TOKEN",tk);
        console.log(tk)
        ```
    - Get network devices: `https://{{DNA_IP}}/dna/intent/api/v1/network-device`
        - Add in headers: `X-Auth-Token:{{DNA_TOKEN}}`
### Python
With the help of cursor and integrated AIs tools we have created a custom API client library to get and post data.
```sh
export DNA_IP=<DNA_IP>
export DNA_USER=<DNA_USER>
export DNA_PASSWORD=<DNA_PASS>
export DNA_SSL=false
python Catalyst_Center/dnaconnect.py

#Resulting output
HOSTNAME  IP ADDRESS  
--------  ------------
sw1       10.10.20.175
sw2       10.10.20.176
sw3       10.10.20.177
sw4       10.10.20.178
```
## Working Catalyst Center with
- Official Cisco Catalist Center Python SDK: 
    - https://dnacentersdk.readthedocs.io/en/latest/
    - https://github.com/cisco-en-programmability/dnacentersdk

### Installation
Execute the command below:
```sh
pip install dnacentersdk
```
Or to Upgrade the libraries to latest version:
```sh
pip install dnacentersdk --upgrade
```
### Script to collect data
```bash
#Linux
export DNA_IP="10.10.20.80"
export DNA_USER="admin"
export DNA_PASSWORD="your_password"
export DNA_SSL="false"
python Catalyst_Center/dnasdk_test.py
```
```powershell
#PowerShell
$env:DNA_IP="10.10.20.80"
$env:DNA_USER="admin"
$env:DNA_PASSWORD="your_password"
$env:DNA_SSL="false"
python Catalyst_Center/dnasdk_test.py
```

### How to get all clients (Special case)
1. Build login and get the token
2. Build a `POST` request with this data:
    - URL: `https://{{DNA_IP}} /api/assurance/v1/host`
    - Use the token previously generated: `X-Auth-Token:{{DNA_TOKEN}}`
    - Add this info in the body:
    ```json
    {
        "starttime":"",
        "endtime":""
    }
    ```
3. With the received information do the count to get the number of Clients

Information collected from here: https://github.com/cisco-en-programmability/dnacentersdk