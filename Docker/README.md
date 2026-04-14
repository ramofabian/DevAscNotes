# Docker
## Computing types
- **Bare metal server**: a physical, single-tenant computer server dedicated to a single customer, offering exclusive access to hardware resources without a virtualization layer (hypervisor).
- **Virtual Machine**: it is a software-based emulation of a physical computer that runs its own operating system and applications, isolated from the host machine. 
- **Container**: it is a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another. 
- **Hypervisor**: Software used manage virtual machines i.e: KVM, VirtualBox, VMWare, etc. This program manages actual server resources by allocating the needed features to each virtual machine, like ram, storage, networking, etc. Depending how powerfull is the server, it will be able to instantiate more VMs deployed in minutes or seconds.
- **Hypervisors types**:
    - *Type A (Bare-metal)*: Exposes the hypervisor directly to the metal server and the VMs. Example: VMWare EXi, Microshodt Hyper-V, Citrix Hypervisor and KVM (Kernel-vased Vistual Machines)
    - *Type B (Hosted)*: It is like a OS which can also run VMs, example: VMware WorkStation, Oracle VirtualBox, Paralles Desktop.
## Docker / Containers
- **Docker**: It is the application which manages *containers*.
- **Image**: It is the encapsulation of sowtware including specific packages and dependecies to be able to run the final application. Then this image used by docker to be able to create the container.
- **Container**: It is lightweight compared with a VM. It *borrows* the underlay OS and kernel to be able to work.
- **Devops role**: Create VMs or containers using automation to delivery them to developers and guarantee it always work.
### Installing Docker on WSL and bate-metal server 
- **Prerequisities**: WSL
- Download docker and install docker desktop for windows with this link: https://docs.docker.com/desktop/setup/install/windows-install/
- To manually install in a bare-metal server use this link: https://docs.docker.com/engine/install/ubuntu/

## Image vs Container
<table>
    <tr>
        <th>Image</th>
        <th>Container</th>
    </tr>
    <tr>
        <td>Temaplate or blueprint to deploy one or multuple containers</td>
        <td>Instance to deploy</td>
    </tr>
    <tr>
        <td>It can be build locally and take another image as a base</td>
        <td>It can configure paramenters to be able to comunicate with others VMs also mount shared folderes in between host OS and contianer</td>
    </tr>
</table>

## Running a python contianer
```sh
#Download an image
docker pull python:3.13.13-alpine
#List all docker images
docker images
#Create a contianer
docker run -dit python:3.13.13-alpine sh
#List all container
docker ps -a
#Stop docker container
docker stop <DOKER-ID/DOCKER-NAME>
#Start an stopped docker container
docker start 5a93eda151e1
#Remove a container (first stop it)
docker rm <DOKER-ID/DOCKER-NAME>
#Remove an image (stop and remove all containers using the image first)
docker image rm image <IMAGE-ID/IMAGE-NAME> 
docker image rmi <IMAGE-ID/IMAGE-NAME> 
```
## Working with networking and storage with docker
- Docker bypasses Linux firewall rules in linux machines
- **-p**: option used to map a port in between local host and the container
- **-v**: option used to map a volume iniside a container
```sh
docker run -d -p 80:80 --read-only -v $(pwd)/nginx-cache:/var/cache/nginx -v $(pwd)/nginx-pid:/var/run nginx

#To see the volumes
docker volume ls
```

## Refernces
- https://www.ibm.com/think/topics/bare-metal-dedicated-servers
- https://docs.docker.com/desktop/
- https://docs.docker.com/engine/install/ubuntu/