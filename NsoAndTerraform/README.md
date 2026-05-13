# Cisco NSO and Terraform
## NSO (Network Services Orchestrator)
- It is an orchestrator of networks
- Link: https://developer.cisco.com/site/nso/
- It manages inventory
- NSO connects into all devices in its own inventory and collect's the running config.
- Components:
    - **Service Manager:** Declare service and its internal aspects (MPLS-L3VPN, LLDP, etc.)
    - **Device Manager:** Assign specific service and additional aspects to devices in the inventory which can be multivendor.
    - **Network Element Drivers (NEDs):** Pre-packets many vendors OS CLI parser to read, push information from the nodes. In addition, NSO needs an input data in a specific data structure (JSON or YAML) to then process it into all needed nodes format.
    - **Central Database (CDB):** Place where running config is kept. This information can be push in to the node and also the node can push configuration on NSO.
### Installing NSO on Ubuntu
- Installation guide: https://nso-docs.cisco.com/guides/administration/installation-and-deployment/local-install
1. Download the installer from official Cisco download center (**Cisco account is required**): https://software.cisco.com/download/home
2. Load the file `nso-6.6-freetrial.linux.x86_64.signed.bin` in the local VM.
3. Update VM: `sudo apt update && sudo apt upgrade -y`
4. Install Java development kit and Java environment: `sudo apt install -y openjdk-17-jdk openjdk-17-jre`
5. Install Python3 and pip3: `sudo apt install python3-pip`
6. Install Pramiko: `pip3 install paramiko`
```sh
#In some cases pip requires a virtual env
mkdir NSO
cd NSO
python3 -m venv NSO
source NSO/bin/activate
pip3 install paramiko
```
7. Fix permission execution for bin file: `chmod +x nso-6.6-freetrial.linux.x86_64.signed.bin`
8. Execute the binary file: `./nso-6.6-freetrial.linux.x86_64.signed.bin --skip-verification`
9. Create installation folder: `mkdir ncs-6.4`
10. Fix permissions to installation binary file: `chmod 777 nso-6.6.linux.x86_64.installer.bin`
11. Execute the installation file: `./nso-6.6.linux.x86_64.installer.bin $HOME/Documents/NSO/ncs-6.4/ --local-install`
12. Create environment variable: `source $HOME/Documents/NSO/ncs-6.4/ncsrc`
13. Create `ncs-run` folder: `ncs-setup --dest $HOME/Documents/NSO/ncs-run`
14. Go to `neds` folder: `cd ncs-6.4/packages/neds`
15. Copy all packets: `cp -r * $HOME/Documents/NSO/ncs-run/packages`
16. Go to NCS-RUN folder: `cd $HOME/Documents/NSO/ncs-run`
17. Run NCS app `ncs`
18. Check NCS status `ncs --status | grep running`

### Synchronizing configurations with NSO
**Prerequisites:** Make sure `ncs` process is running.
**Procedure:**
- Connect to NSO CLI: `ncs_cli -C -u admin`
- Ensure all packets are loaded: `packages reload`

### Creating an inventory
- Check inventory status: `show devices list`
- Steps to create inventory:

1. Configure authentication for the group of devices.
```sh
config
devices authgroups group <GROUP-NAME> default-map remote-name <USER-NAME> remote-password <PASSWORD>
commit
exit
```
2. Then add devices to those groups.
```sh
#Addi new device to inventory
device <DEVICE-NAME> address <REMOTE-HOST-IP> authgroup <GROUP-NAME> device-type <CLI/NETCONF/SNMP> ned-id <NED-ID>
device R1 address 192.168.1.23 authgroup mygroup device-type cli ned-id <NED-ID>
#Enable changes in remote device
state admin-state unlocked
exit
```
3. Fix SSH algorithms
```sh
devices global-settings ssh-algorithms public-key ssh-rsa
devices global-settings ssh-algorithms public-key ssh-ess
commit
``` 
4. Check inventory
```sh
show devices list
```
5. Fetch `SSH` keys:
```sh
devices device <DEVICE-NAME>
ssh fetch-host-keys
exit
exit
```
6. Display running config (it shouldn't display actual configuration because NSO is out-of-sync)
```sh
show running-config devices device <DEVICE-NAME> config
``` 
7. Sync NSO DBs
```sh
config 
devices device <DEVICE-NAME>
#Save configuraiton in NSO
sync-from
exit 
exit
```
8. Check inventory
```sh
show devices list
```
### Sync configuration from NSO
- To check if the devices are in sync: `devices check-sync`
- To see what exactly is out-of-sync: `devices device <HOST_NAME> compare-config`
- To test the fix:
```sh
conf
devices device <HOST_NAME>
sync-to dry-run
# To display the config in cisco cli format
sync-to dry-run { outformat native}
# Push the configuration to the ROUTER before the change
sync-to
```  
## Terraform
- Automation software created by HashiCorp: [Official website](https://developer.hashicorp.com/terraform)
- Similar application to what is Ansible, but its specialty is for cloud environments.
- Terraform config files are contained by files with `.tf` extension
    - It uses HashiCorp configuration language.
    - It is similar to `json` formatting.
### Installation
- Link: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli
- Windows: `choco install terraform`

### Files
- Files structure:
    - `terraform.tf`
    - `main.tf`: Main logic to create the virtual machines or any other activity.
    - `Provider.tf`: Contains provider and connection access details. 
    - `variables.tf`: List and definition of every variable.
    - `outputs.tf`: Print on `cli` information 

### Execution
- Initiate terraform project: `terraform init`
- Review and create a plan for the execution: `terraform plan -out=<folder> -var=<var_in_varriables_file>=$<local_env_var>`
- Make the actual deployment: `terraform apply <plan-name>`
- Remove the deployment: `terraform destroy <plan-name>`