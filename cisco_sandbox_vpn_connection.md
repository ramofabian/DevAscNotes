# Procedure to install cisco VPN on Ubuntu 24.04
This is a procudure applicable for all folks who doesn't have th money to pay for a Cisco Anyconnect license to be able to use it to connect to Cisco Sandbox labs which requires VPN to be able to connect to the lab.

<b>Note:</b> 

## Requirements
- Ubuntu 24.04
- User with sudo privileges.
- Internet access.

## Open connect client installation
1. Update the system
```sh
$ sudo apt update
$ sudo apt upgrade
```
2. Install OpenConnect client
```sh
$ sudo apt install openconnect
```
3. Connect to Sandbox VPN
```sh
sudo openconnect -b <VPN_IP_OR_URL>
```
If the vpn tunel was successfylly establised the output below should be seen and you need to save the `pid` ID:
```shell
Got CONNECT response: HTTP/1.1 200 CONNECTED
CSTP connected. DPD 90, Keepalive 60
No DTLS address
Set up UDP failed; using SSL instead
Configured as 192.168.1.13, with SSL connected and DTLS disabled
Continuing in background; pid 1650
```
3. To stop the connection
Identify the pid ID:
```sh
$ sudo ps -aux |grep openconnect
```
Kill connection by using PID ID:
```sh
#option 1
sudo pkill openconnect
#option 2
sudo kill <PID_ID>
```

## References
1. [Official Devnet documentation](https://developer.cisco.com/docs/sandbox/getting-started/#sandbox-vpn-info)
2. [OpenConnect installation](https://www.howtoforge.com/how-to-install-openconnect-vpn-server-on-ubuntu-22-04/)