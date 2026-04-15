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
docker pull <IMAGE-NAME>
docker pull python:3.13.13-alpine
#List all docker images
docker images
#Create a contianer and downloads the image if it is not available locally
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
- **--restart**: option to make the container to be up under certains conditions:
    - *no*: Don't automatically restart the container. (Default)
    - *on-failure[:max-retries]*: Restart the container if it exits due to an error, which manifests as a non-zero exit code.
    - *always*: Always restart the container if it stops. If it's manually stopped, it's restarted only when Docker daemon restarts or the container itself is manually restarted. 
    - *unless-stopped*: Similar to always, except that when the container is stopped (manually or otherwise), it isn't restarted even after Docker daemon restarts.
```sh
docker run -d -p 80:80 --read-only -v $(pwd)/nginx-cache:/var/cache/nginx -v $(pwd)/nginx-pid:/var/run nginx
#Example1
docker run -d --restart unless-stopped -p 80:80 -v $(pwd)/nginx-cache:/var/cache/nginx -v $(pwd)/nginx-pid:/var/run nginx 
#Example2
docker run -v $(pwd)/my_folder:/root/my_folder -dit python:3.13.13-alpine sh
#To see the volumes
docker volume ls

```
## Building docker images
### Docker Hub
- Platform used to share official and not official docker images with everybody like github. It is call docker registry.
- Docker images in docker hub can be public or private. The private version has charges.

### Small API
- This time we will be creating an docker container with a small api inside. To be able to do it we will be using FAST API.
- Reverse proxy `uvicorn` to handle web request.
- **Reverse proxy:** A reverse proxy is a server that sits in front of one or more web servers and acts as a gateway.
### Prerequisities 
```sh
pip install fastapi
pip install uvicorn
```
### Starting  Web API 
```sh
cd /Docker/mySmallApi
uvicorn  main:app --host 0.0.0.0 --port 8000
```
### Docker File
```sh
#Base image and specific platform linux/amd64 to be supported
FROM --platform=linux/amd64 python:3.11-slim
#Adding a working directtory
WORKDIR /app
#Installing pre-requisites
#Disclamer: We can use ADD instead of COPY but it is not recommended as it can cause issues with caching and file permissions. Also it can used to download files.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt #--> Used when building the container only
#Coping the API script
COPY app/ .
#Exposing the port 8000
EXPOSE 8000
#Running reverse proxy
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] #--> Used after starting the container
```

### Building the docker image
- Make sure docker deamon is working correctly and if it is needed dockerhub connection login locally with your own credentials
```sh
#Command to see if docker client and server are running ok
docker info
#Command to login on dockerhub from cli
docker.exe login -u <dockerhub-user>
```
- Commands to build the image
```sh
#Command with dockerhub username, to then push it on dockerhub
docker build -t <docker-hub-username>/demofastapi:v0.0.1 .
#Command to just keep the image in local registry
docker build -t demofastapi:v0.0.1 .
#No errors should bee seen during the building process
#Check the generated image
docker images
```

### Deploying the container
```sh
#deploy the container 
docker  run -p 8000:8000 demofastapi:v0.0.1
#With deatach mode enable
docker  run -d -p 8000:8000 demofastapi:v0.0.1
#check api response
curl -k http://localhost:8000
curl -k http://localhost:8000/health
```

### Pushing an image on Docker Hub 
- It is mandatory local login with docker hub credentials with the command: `docker.exe login -u <dockerhub-user>`
```sh
docker push <docker-hub-username>/demofastapi:v0.0.2
```

### Eample
- Docker image which prints hello world messages on cli
- python script:
```py
print("Hello, World!")
print("""
    *     *
   / \   / \
  /   \ /   \
 |  ^  ^  ^  |
 |  o  o  o  |
  \  ~~~~~  /
   \_______/
""")
```
- docker file:
```sh
#Base image
FROM --platform=linux/amd64 python:3.11-slim
#Adding a working directtory
WORKDIR /app

COPY hello_world.py .

CMD [ "python", "hello_world.py" ]
```
- Building the image
```sh
docker build -t <docker-hub-username>/demopyhello:v0.0.1 .
```
- Verifying that the is working fine:
```sh
docker run  <docker-hub-username>/demopyhello:v0.0.1
```
- Pushing the image on docker hub:
```sh
docker push <docker-hub-username>/demopyhello:v0.0.1
```

## Refernces
- https://www.ibm.com/think/topics/bare-metal-dedicated-servers
- https://docs.docker.com/desktop/
- https://docs.docker.com/engine/install/ubuntu/
- https://medium.com/@uzair-jawaid_26268/reverse-proxies-what-they-are-and-how-to-build-one-2b94500612fc
- https://docs.docker.com/engine/containers/start-containers-automatically/#use-a-restart-policy