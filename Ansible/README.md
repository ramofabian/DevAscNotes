# Ansible
- It is an application that can run on a server or desktop.
- It supports Windows (WSL) or Linux.
- Ansible is agentless.
- Main propuse is the automation of massive deployment of infrastructure by configuring servers, swtiches, routers, etc.
- It uses the concept of **task** for any specific objective we want to achive. i.e. Installing docker in 50 servers.
- To be able to execute the `task`, it is required an **inventory** where all host IPs, users, passwors will be allocated.
- With the task or list of tasks and the inventory, during the execution Ansible will connect in parallel to all devices and execute each task in a sequencial way.
- **Idenpotent behaviour**:  ensures that performing an operation multiple times produces the same result as performing it once, preventing unintended side effects from repeated actions.
- All files are in **yaml** formating.
- **Playbook**: Defines a list of tasks, which machines we want to connect to by pointing them from our inventory.
- **Variables**: Additional information used to deploy information host specific or group specific.
- **Configuration file**: it is the `ansible.cfg` file use to st global parameter to be able to run the playbook without any issue. i.e: disbale ssl cerificates, connect under specific conditions.

## Configuring enviroment topology
- Install `containerlab`:
```sh
curl -sL https://containerlab.dev/setup | sudo -E bash -s "all"
```
- Create custom docker images for ansible container and client containers:
```sh
#Docker file for ubuntu server where ansible will be installed
FROM ubuntu
RUN apt-get update &&\
    apt install python3 ansible openssh-client vim iputils-ping -y
EXPOSE 22

#Docker file for client container
FROM ubuntu
RUN apt-get update &&\
    apt install python3 ssh vim -y
EXPOSE 22

#Building docker images
docker build -t <dockerhub-user>/ubuntuserver:v0.0.1 -f dockerfile_ansible .
docker build -t <dockerhub-user>/ubuntuclient:v0.0.1 -f dockerfile_client .
```
- Topology definition:
```yml
# Ansible topology using contianerlab
name: ansible-lab

topology:
  kinds:
    linux:
      image: docker.io/library/ubuntu:latest
  nodes:
    ansible:
      kind: linux
    client1:
      kind: linux
    client2:
      kind: linux
    client3:
      kind: linux
    client4:
      kind: linux

  links:
    # client connection links
    - endpoints: ["client1:eth1", "client2:eth2"]
    - endpoints: ["client2:eth1", "client3:eth2"]
    - endpoints: ["client3:eth1", "client4:eth2"]
    - endpoints: ["client4:eth1", "client1:eth2"]
```

- Deploy the topology:
```sh
clab deploy -t ansible-lab-topo.yaml
```
- Check all assigned IPs and FQDNs: 
```sh
cat /etc/hosts
#In my case this is the assignation given by the CLAB
###### CLAB-ansiblelab-START ######
172.20.20.4     clab-ansiblelab-client2 977071b9b791    # Kind: linux
172.20.20.5     clab-ansiblelab-client3 6369161fc628    # Kind: linux
172.20.20.2     clab-ansiblelab-client4 17a98cedd46e    # Kind: linux
172.20.20.3     clab-ansiblelab-ansible 39014d6dea0b    # Kind: linux
172.20.20.6     clab-ansiblelab-client1 2d76434f4d71    # Kind: linux
```
- Connect to Anssible container and configure a root password
```sh
docker exec -it clab-ansiblelab-ansible /bin/bash 
#Configure root pasword
passwd root
#Update the OS
apt update -y
#Install openssh
apt install openssh-server -y
``` 


## Installing ansible
- Install ansible
```sh
#Ubuntu command
sudo apt install ansible -y
```
- Configure passwordless in between ansible machine and target machines
```sh
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
#OPTIONAL BUT POTENTIALLY NEEDED
chmod 600 ~/.ssh/id_rsa
#Copy ssh-key from origing to any destination server/container/VM/host computer
ssh-copy-id -i ~/.ssh/id_rsa.pub tim@just.some.other.server
```

## References
- https://medium.com/@arundpatil007/understanding-idempotence-a-key-concept-in-computer-science-fe5dc69877c6
- https://containerlab.dev/
- https://naveenkumarjains.medium.com/ansible-setup-on-containers-4d3b3efc13ea