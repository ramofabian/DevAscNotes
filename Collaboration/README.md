# Cisco Collaboration
Official information link: https://www.cisco.com/site/us/en/products/computing/servers-unified-computing-systems/index.html
## UCS (Unified Computing System)
- UCS is a server
- It has applications in DC and other enviroments
- It brings services in: compute networking and storage.
- Single point of interface management for the DC network.
- Supports integration with AI (AI PODs).
### UCS Family
- UCS X-Series Modular system (For hybrid cloud)
- UCS B-Series Modular system (Blade servers)
- UCS C-Series Modular system (Rack server)
- UCS S-Series Modular system (Storage server)
### Management platforms
- Cisco intersight (Cloud controller)
```sh
                                +------------------+
                                | Cisco Intersigth |
                                |  SDN controller  |
                                +------------------+
                                          |
              ------------------------------------------------------------
              |                                                          |
       +-------------+                                           +--------------+
       | UCS Manager |                                           | UCS Director |
       +-------------+                                           +--------------+
              |                                                         |
            Tasks                                                     Tasks
              |                                                         |
+---------------------------+                               +---------------------------+
| Manage compute layer for: |                               | Manage compute layer for: |
| |_Provissioning           |                               | |_Provissioning           |
| |_Policies                |                               | |_Policies                |
| |_Monitoring              |                               | |_Monitoring              |
+---------------------------+                               | |_Vendor agnostic !!      |
                                                            +---------------------------+
```
### UCS SDK (SOAP API with RPC and XML)
- Python: `ucsmsdk` https://github.com/CiscoDevNet/intersight-python
- PoweShell: `Powertoll`   https://github.com/CiscoDevNet/intersight-powershell

### Cisco Intersigth Restfull API
- Offical documentation link: https://intersight.com/apidocs/introduction/overview/
- Supports:
  - Cisco UCS
  - Cisco HCI
  - Cisco MDS
  - Cisco UCS Director
  - Intersight Cloud Orchestrator
  - Intersight Workload Optimizer
  - VMware vCenter
  - Storage System
- Restfull API:
  - Everithing is managed as an object
  - Uses RSA Key pairs to handle the connection
  - It can boot devices from boot api
### AXL API SOAP API
- Used with Cisco CUCM's SOAP-based Administrative XML Layer (AXL) API.
- Simmilar utilization as NETCONF but more explicit.
- Inside of <get-data> there is a unique rpc for the specific action to be executed, like: getUser, getCompute, getPresence.
- It operates over `HTTPS` and supports `POST` request only.
- It requires basic authentication.
- `WSDL` its a file where can be seen all rpc methods, all optenial operations and parameters.
  - To get the file:
    1.  go to CUCM GUI, go to Application, then Plugins.
    2. New window pop's up and click on Fund button.
    3. Download the Cisco ACL toolkit
    4. Open the downloaded file and go to: schema -> <version> -> AXLAPI.wsdl to find the WSDL file.
    5. To see the conten of the file use `SoapUI` to see the information. -> [LINK](https://www.soapui.org/)
### UDS REST API
- Used with User Data Services (UDS) API for `CUCM`.
- Mainly used for `rea-only` operations (`GET` requests).
- Check the user profile and make sure the account is part of `Standard CCM End Users` or `Standard CCM Admin Users` Permission Group.
- It requires basic authentication.
- In the headers section must be included: `{'Accept':'application/xml', 'Content-type':'application/xml'}`
- Endpoints:
  - To get the full list of users: `https://<URL>:8443/cucm-uds/users` 
  - To get the full list of servers: `https://<URL>:8443/cucm-uds/servers` 
  - To get the full list of user details: `https://<URL>:8443/cucm-uds/user/<USER_NAME>` 
  - To get the full list of user speed dial details: `https://<URL>:8443/cucm-uds/user/<USER_NAME>/speedDials` 
  - To get the full list of devices from some specific user: `https://<URL>:8443/cucm-uds/user/<USER_NAME>/devices` 