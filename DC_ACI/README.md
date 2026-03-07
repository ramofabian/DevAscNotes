# ACI Data Center controller
- Sowftware defined controller
- ACI stands for: Application Centric Infrastructure
- Componenets:
    - Fabric (Nexus 9K devices)
        - Routing protocols:
            - Point2Point links are L3 and runs `OSPF` or `IS-IS` (UNDERLAY)
            - Tunneling created with `VXLAN` and `BGP-EVPN` (OVERLAY)
        - CLOS achitecture (Leaves NX 9.3K and Spines NX 9.5K)
        - `VXLAN` used to tunnel the frames from one end to another end (ends could be any leaf or Spine)
        - ECMP is used to have path full redundacy
        - Endpoints:
            - Baremetal servers
            - VMs workloads
            - Container Workloads
            - APIC Cluster
            - Load balancers services
            - External L3Out (Legacy DCs)
    - Aplication Policies
        - Policies are dinamically deployed based on applications running behind the fabric.
        - APIC:
            - Cisco UCS servers running application policy cluster
            - It uses NXAPI-REST to manage the Nexus 9k.
    - Controller
## Application Policies
- Tenants DCs can manage thousands of tenants and those not always talk eache other.
- Structure:
    - Uni is equal to sys from api app
    - DN = distinguish name
    - Tenant:
        - Creates a boundary that separates differents groups or customers ensuring their applications do not interact unless explicity configured
    - Policy:
        - EPG = Endpoint group
            - By default they are not allowed to talk with anything outside of group
        - Contract:
            - Roules indicating which other EPGs can communicate each other
        - Filters (ACLs)
            - There is posibility to apply primary and secondary filter
    - Network:
        - VRFs, bridge doamins, subnets and external networks definitions
        - Notes: 
            - EPG belongs to bridge domains
            - Subnets are attached to VRFs and bridge domains.
```sh
            Uni == (sys in nxapi)
+------------------+------------+-------------+
|  Tenant Common   |  Tenant A  |  Tenanat B  |
+------------------+------------+-------------+

#Detail:
        +------------+
        |  Tenant A  |
        +------------+
               |
               |
    +----------------------------+
    | NETWORK     |    Policy    |
    +-------------+--------------+
          |              |
          |              |
          |      +-----------------------------+
          |      |    Application Profile      |
          |      |     QoS and FW rules        |
          |      |     EPGs (Endpoints groups) |
          |      +-----------------------------+
          |
  +------------------------+
  |  VRFs (Routing domain) |
  |  Bridge Domains (L2)   |
  |  Subnets               |
  |  Esternal Networks     |
  +------------------------+
```
## APIC Object Model
- it uses visore as NX-API do `https://<ACI_IP>/visore`.
- It has an API inspector to see all requiest in real time.
- `uni` = This is the root and `MO`
- Searching classes:
    - Almast always classes contains modules and all of them have a prefix of `fv` or incase onf contracts it is `v2`
    - We need to search by classes like:
        - Tenant
        - Bridge Domain
        - Subnet
        - Aplication profile = Ap
        - Epg = AEPg
        - Endpoint group = CEp
        - Ip Address = IP
        - Contract = BrCP
    - Examples:
        - fvTenant
        - fvSubnet
- Searching objects:
    - It has prefixes likeL
        - `tn`+`Name` = tenant
        - `BD`+`Name` = Bridge domain
        - `ap`+`Name` = Application profile
        - `epg`+`Name` = EPG
        - `cep`+`Name` = Endpoint group

## Working with APIC API
- Login method is via token authentication.
    - We connect by using authorized account and request a token.
    - With the token ID and based on the implemented policies API calls can be executed.
    - Token ID has expiration time, it must be renewved before this time ends.
- Endpoints to collect and login:
    - For login and get a token: `https://{{apic}}:{{apic_port}}/api/aaaLogin.json` (`POST` request with body should be same as NX-API-login)
    - Tenant list: `https://{{apic}}:{{apic_port}}/api/class/fvTenant.json` (`GET` request with token included on headers and cookies)
    - Application profile list: `https://{{apic}}:{{apic_port}}/api/class/fvAp.json` (`GET` request with token included on headers and cookies)
    - Listing all applications profiles for a specific tenant: `https://{{apic}}:{{apic_port}}/api/node/mo/<TENANT_NAME>/ap-access.json` (`GET` request with token included on headers and cookies)
- Endpoints to create objects:
    - Createring a tenant: `https://{{apic}}:{{apic_port}}/api/node/mo/uni.json` (`POST` request with token included on headers and cookies)
        Body:
        ```json
        {
            "fvTenant":{
                "attributes":{
                    "dn":"uni/tn-Storage",
                    "name":"storage",
                    "rn":"tn-Storage",
                    "status":"Created"
                },
                "children":[]
            }
        }
        ```
- Python script to collect and list all tenants configured on the ACI
```sh
#Create virtual enviroment variables (Linux)
export APIC_HOST_ENV = "APIC_HOST"
export APIC_USERNAME_ENV = "APIC_USERNAME"
export APIC_PASSWORD_ENV = "APIC_PASSWORD"
export APIC_SSL_VERIFY_ENV = "APIC_SSL_VERIFY"
python DC_ACI/acisimple.py
```
```powershell
#Create virtual enviroment variables (Windows)
$env:APIC_HOST_ENV="APIC_HOST"
$env:APIC_USERNAME_ENV="APIC_USERNAME"
$env:APIC_PASSWORD_ENV="APIC_PASSWORD"
$env:APIC_SSL_VERIFY_ENV="APIC_SSL_VERIFY"
python DC_ACI/acisimple.py
```
## SDKs for ACI
There are 2 SDKs for ACI:
- ACI Toolkit (Old version) --> [LINK](https://github.com/datacenter/acitoolkit)
- Cobra (new version but available only from physical APIC controller) --> [LINK](https://cobra.readthedocs.io/en/latest/)
- PyACI (Lightweight Python library for ACI REST API) --> [LINK1](https://github.com/datacenter/pyaci), [LINK2](https://pyaci.readthedocs.io/en/latest/)
- Cisco ACI Ansible Collection (For automation workflows) --> [LINK](https://galaxy.ansible.com/cisco/aci)
- Cisco ACI Terraform Provider (For Infrastructure as code) --> [LINK1](https://registry.terraform.io/providers/CiscoDevNet/aci/latest), [LINK2](https://aci-prog-lab.ciscolive.com/lab/pod23/netascode/nac-run)
- Network-as-Code (NAC) (Declarative YAML-based configuration) --> [LINK](https://netascode.cisco.com/)

