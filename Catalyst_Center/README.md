# Automate with Catalyst Center and DNA
- SDN controller
- It is use for Catalyst 9000
- Attach policies becased on a predefined place, this policy contians parameter which will chege if the same aplication is moved to another location.
- It uses LISP (location ID) + VXLAN + IS-IS

## 5 Applications
1. Desing: Global layout, name address.
2. Policy: Group based access control and IP and URL Based Access Control
3. Provision: Inventory (discovery), Software defined Access layer, Wrielless.
4. Assurance: Heath and analytics
5. Platform: System API
    - North-south API
        - Northbound API - Client computer/server
        - Southbound there is Infra
    - East API -> EVENT -> Outgoing external Aplications (webhooks)
    - West API Input external aplications -> Aplications where Catalist Center relays on.
        - Cisco ISE (AAA)
        - DHCP (IPAM)
        - DNS
    - Path: Platform/Developer toolkit (API DOC/Swagger documentation)
## Working Catalyst Center with Postman and python 
- Endpoint definition:
    ```sh
      https://{{DNA_IP}}/dna/system/api/v1/auth/token
              |_________|_________________|__________|
                  |            |               |->Sub module section
                  |            |->Main module section: system, intent, etc..
                  |-> FQDN/IP
    ```
### Postman
1. Create DNA collection and enviroment.
2. Create enviroment variables:
    - `DNA_IP`
    - `DNA_USER`
    - `DNA_PASSWORD` (enable encription)
    - `DNA_TOKEN` (enable encription)
3. Make sure the created enviroment is created.
4. Requests:
    - Login: `https://{{DNA_IP}}/dna/system/api/v1/auth/token`
        - `POST` request
        - Enable basic authentication and add user and password
        - JavaScript to extract the topken from body response into `DNA_TOKEN`
        ```js
        var jsonData = pm.response.json();
        var tk = jsonData.Token;
        pm.environment.set("DNA_TOKEN",tk);
        console.log(tk)
        ```
    - Get network devices: `https://{{DNA_IP}}/dna/intent/api/v1/network-device`
        - Add in headers: `X-Auth-Token:{{DNA_TOKEN}}`
### Python
With the help of cursor and integrated IAs we have created a custom API client library to get and post data.
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
Or to Upgrade the libraries to lates version:
```sh
pip install dnacentersdk --upgrade
```
### Script to collect data
```bash
#Linux
$env:DNA_IP="10.10.20.80"
$env:DNA_USER="admin"
$env:DNA_PASSWORD="your_password"
$env:DNA_SSL="false"
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