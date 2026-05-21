# IP and subnetting
## IPV4 Private ranges
- Used for internal WAN and LAN connection and it is not shared with internet.
- Reserved ranges:
    - 10.0.0.0/8
    - 172.16.0.0/12 - 172.31.255.255/12
    - 192.168.0.0/16
## IPV4 Public ranges
- Unique ip address or group of ip addresses.
- It used to have internet connectivity.
- It is allocated by SP (Service providers) or local government entity ruling the IP allocation.

## NAT
**NAT:** Network address translation.
    - Requires on IP address (IPv6 or IPv4, and it could be public or private) with WAN access or internet access.
    - Private ip pools with allocated ranges mapped in one router.
- Translation between private and public address.
- It is used by the firewall or router.

## Network masks
- **Masks:** Indicates which bits are locked
- slash notation: i.e /26, /17, /28
    - /8 = Class A
    - /16 = Class B
    - /24 = Class C 
- doted notation: 255.255.255.255 
    - 255.0.0.0 = Class A
    - 255.255.0.0 = Class B
    - 255.255.255.0 = Class C



