# Atomating with Cisco IOS-XE

## YANG and Netconf with IOS-XE
Pre-requisites:
1. eve-ng hosted locally or on cloud.
2. CRs1000v with IOS-EX 16.x or newer. [eve-ng images link](https://github.com/hegdepavankumar/Cisco-Images-for-GNS3-and-EVE-NG?tab=readme-ov-file)
3. Internet or local ssh connection 

<b>Notes:</b> 
- Link of supported HW for IOS-XE [link](https://www.cisco.com/site/us/en/products/networking/cloud-networking/ios-xe/index.html)
- Optionally if there is not access to eve-ng, use cisco sandbox.

<img src="Pictures/lab1_ios_xe.png" alt="isolated" width="200"/>

### YANG Model
YANG models defines how the data should be structured to be able to interact with some specific vendor equipment, it is ussually created by the vendor itself.
Link to all official available models: https://www.netconfcentral.org/

Those YANG modules convert the commands outputs in XML or JSON which is more friendly for the application to process it. There are standards ruled by IEEE and IETF which dictate the basicis for verdor's YANG models should be created and worked to make it easy to parse it in a multiverndor network.

### NETCONF Protocol
- Protocol used to interact with network elements in similar way as SSH does.
- `TCP` based protocol, by default it uses the port `830`
- It runs on top of `SSH` (it means, netconf behavies same as SSH protocol exchanging keys)
- It uses `RPC` (Remote Procedure Calls) to interact with the NEs.
- When the connection is establised, the NE will reply with the list of capabilities (List of supported YANG models).
- When an `RPC` is send, the origin adds on the header a message-id with a ramdom value. Once it is received and the NE replies to it, it uses the same message-id.

#### RPC (Remote Procedure Calls)
- It is a built in command to get or push data by using YANG model.
- Type of commands:
    - `get`: Get operational state information
    - `get-config`: Get configuration
    - `set-config`: Push confguration

```xml
<rpc>
    <get>
        <data>
            #|---> YANG DATA FORMAT!!
        </data>
    </get>
</rpc>
```
### Pyang (Python library for YANG models)
1. Go to netconf folder: `cd IOX-XE/netconf`
2. Clone the git repo: `git clone https://github.com/YangModels/yang.git`
3. Create your own venv if it wasn't created already and make it active.
4. Install pyyang: `pip install pyang`
5. Go to vendor folder: `cd yang\vendor\cisco\xe`
6. Go to the user software version folder. i.e.: `ll xe/1731/` check all listed yang models
7. To view the model: `pyang.exe -f tree Cisco-IOS-XE-interfaces-oper.yang`

<b>Optional:</b> We can use yangsuit to check the Cisco YANG models: https://developer.cisco.com/docs/yangsuite/


### CSR1 configuration
Command list:
```bash
#Check ip and port status
ena
show ip interface brief

#Configure hostname
conf t
hostname CSR1

#Configure ssh access
ip domain name crdevnet.com
crypto key gen rsa mode 2048
line vty 0 4
login local
transport input ssh
exit

#Configuring use/passowrd
username admin priv 15 secret password

#Configure NETCONF
netconf-yang
```
### CSR2 configuration
Command list:
```bash
#Check ip and port status
ena
show ip interface brief

#Configure hostname
conf t
hostname CSR2

#Configure ssh access
ip domain name crdevnet.com
crypto key gen rsa mod 2048
line vty 0 4
login local
transport input ssh
exit

#Configuring use/passowrd
username admin priv 15 secret password

#Configure NETCONF
netconf-yang
```

### Collecting data with NETCONF
Execute python  script to collect interface information from the remote node:
1. Connect via CLI to CSR1 and CSR2, collect management IP (In this case is the DCHP IP running on port Gi0/0).
2. Open the python script at `IOS-XE\netconf\connec.py` replace the IP and credentials acordingly.
```py
DEVICE = {
        "host": "192.168.160.134",  # TODO: change to your device IP / hostname
        "username": "admin",   # TODO: change to your username
        "password": "password",   # TODO: change to your password
        "port": 830,
    }
```
3. Install libraries: `pip install ncclient xmltodict`
4. Execute the script: `Python IOS-XE\netconf\connec.py`. The output will look like this:
```bash
Interface           IP-Address        OK?   Method  Status      Protocol
--------------------------------------------------------------------------
GigabitEthernet1    unassigned        YES           if-oper-state-readyif-state-up
GigabitEthernet2    unassigned        YES           if-oper-state-no-passif-state-down
GigabitEthernet3    unassigned        YES           if-oper-state-no-passif-state-down
GigabitEthernet4    unassigned        YES           if-oper-state-no-passif-state-down
(venv)
```

### Push data with NETCONF onto remote node
Execute python script to provision 2 loopbacks IPs in 2 diffenten interfaces in the remote node:
1. For security best practices, we need to avoid the utilization of credentials, IPs inside of script code. To avoid it, we can use enviroment variables in linux and windows.

Linux
```bash
export NETCONF_HOST="x.x.x.x"
export NETCONF_USER="admin"
export NETCONF_PASS="password"
python .\IOS-XE\netconf\setloop.py
```
Powershell
```powershell
$env:NETCONF_HOST="x.x.x.x"
$env:NETCONF_USER="admin"
$env:NETCONF_PASS="password"
python .\IOS-XE\netconf\setloop.py
```
2. Execute the script: `Python IOS-XE\netconf\setloop.py`. The output will look like this:
```bash
#EXECUTION LOG
Loopback1 -> 10.10.10.2/255.255.255.255
Loopback2 -> 10.10.10.1/255.255.255.255
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:dc376de6-2b84-4035-8da8-2b4d14bd3069" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"><ok/></rpc-reply>
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:66f0a3fb-5842-4029-9028-801e8457881d" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"><data><native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"><interface><Loopback><name>1</name><ip><address><primary><address>10.10.10.2</address><mask>255.255.255.255</mask></primary></address></ip><logging><event><link-status/></event></logging></Loopback><Loopback><name>2</name><ip><address><primary><address>10.10.10.1</address><mask>255.255.255.255</mask></primary></address></ip><logging><event><link-status/></event></logging></Loopback></interface></native></data></rpc-reply>
(venv) 
```
CLI info:
```
CSR1#show ip int brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       192.168.160.134 YES DHCP   up                    up
GigabitEthernet2       unassigned      YES NVRAM  administratively down down
GigabitEthernet3       unassigned      YES NVRAM  administratively down down
GigabitEthernet4       unassigned      YES NVRAM  administratively down down
Loopback1              10.10.10.2      YES other  up                    up
Loopback2              10.10.10.1      YES other  up                    up
CSR1#

```