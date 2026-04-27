# Automating networks with Ansible
- Software development life cycle enviroments:
    - **Dev:**
        - Local computer usully used with a very minimalistic setup.
        - It is the enviroment where developers can run tests during the code development
        - Once the dev enviroment completes on module or all works, it pushes the code to test enviroment.
    - **Test:**
        - In test enviroment there is a lab with a topology the most closer to production enviroment.
        - Here we can count with a server where Ansible and some other services are running, routers and switches.
        - Emualting software can be used like: Eve-ng, Cisco Modeling Labs, GNS3, PnetLabs.
        - After testing is done, code is pushed to production.
    - **Prod:**
        - Real server where Ansible will be running.
        - Real network working
## Ansible Networking Modules
- Ansible network modules: [Link](https://docs.ansible.com/projects/ansible/2.9/modules/list_of_network_modules.html)
- All availbale Modules: [Link](https://docs.ansible.com/projects/ansible/2.9/modules/modules_by_category.html#module-index)
- Ansible `state` options:
    - *Merged*: Update the config lines that changes if it existis or create it if doesn't exists with the provided data.
    - *Replace*: Delete the previous config and add the new configuration 
    - *Overridden*: Delete all objects under the same context and configure the objects listed.
    - *Delete*: Remove specific configuration.

## Lab topology using eve-ng
### Preparation
- 4x CSR1000v version 17.03.05
- Internet connection
- Linux server 

<img src="Pictures/topology1.png" alt="isolated"/>

- Add initial configuration to enable ssh and netconf access:
```sh
#R3
#Check ip and port status
ena
show ip interface brief
#Configure hostname
conf t
hostname CSR3
#Configure ssh access
ip domain name crdevnet.com
crypto key generate rsa modulus 2048
line vty 0 4
login local
transport input ssh
exit
#Configuring user/password
username admin priv 15 secret password
do sh run | include http
#Configure NETCONF and RESCONF
netconf-yang
restconf
exit

#R4
#Check ip and port status
ena
show ip interface brief
#Configure hostname
conf t
hostname CSR4
#Configure ssh access
ip domain name crdevnet.com
crypto key generate rsa modulus 2048
line vty 0 4
login local
transport input ssh
exit
#Configuring user/password
username admin priv 15 secret password
do sh run | include http
#Configure NETCONF and RESCONF
netconf-yang
restconf
exit

#R5
#Check ip and port status
ena
show ip interface brief
#Configure hostname
conf t
hostname CSR5
#Configure ssh access
ip domain name crdevnet.com
crypto key generate rsa modulus 2048
line vty 0 4
login local
transport input ssh
exit
#Configuring user/password
username admin priv 15 secret password
do sh run | include http
#Configure NETCONF and RESCONF
netconf-yang
restconf
exit

#R6
#Check ip and port status
ena
show ip interface brief
#Configure hostname
conf t
hostname CSR6
#Configure ssh access
ip domain name crdevnet.com
crypto key generate rsa modulus 2048
line vty 0 4
login local
transport input ssh
exit
#Configuring user/password
username admin priv 15 secret password
do sh run | include http
#Configure NETCONF and RESCONF
netconf-yang
restconf
exit

```
### Inventory
- Optional, if we want to run acual CLI command we can use the option: `network_cli`. It can parse the output.
- In local folder create inventory directory and file:
```yaml
all:
  childen:
    ios_xe_routers:
      hosts:
        ios-xe-3:
          ansible_host: 192.168.160.133
          ansible_user: admin
          ansible_password: password
          ansible_network_os: iosxe
          ansible_connection: netconf
        ios-xe-4:
          ansible_host: 192.168.160.130
          ansible_user: admin
          ansible_password: password
          ansible_network_os: iosxe
          ansible_connection: netconf
        ios-xe-5:
          ansible_host: 192.168.160.131
          ansible_user: admin
          ansible_password: password
          ansible_network_os: iosxe
          ansible_connection: netconf
        ios-xe-6:
          ansible_host: 192.168.160.139
          ansible_user: admin
          ansible_password: password
          ansible_network_os: iosxe
          ansible_connection: netconf

```
- Test ansible server connection against all nodes:
```sh
#Execut ping to remote end
ansible -i inventory/inventory.yaml ios_xe_routers  -m ping
(ansible-lab) devnet@devnet-VirtualBox:/Lab01$ ansible -i inventory/inventory.yaml ios_xe_routers  -m ping
ios-xe-3 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
ios-xe-5 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
ios-xe-6 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
ios-xe-4 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

# Gather all facts from remote devices
ansible -i inventory/inventory.yaml ios_xe_routers  -m ansible.builtin.setup
```
### Playbook to gather all facts
- 