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

# Firewall
- Used in:
    - Internet edge
    - DC (data center) edge
- Manages access control
    - Access control list: ACL
        - Who can access what:
            - IP address (subnets)
            - TCP/UDP port 
- Other services:
    - VPN termination
    - DMZ (Demilitarized zone)
        - Additional network where local applications can be accessed from public networks. 
    - L3 capable:
        - Can run L3/L2 protocols.

- NGFW (Next generation firewall)
    - It has more features than normal firewall.
        - IPS (Intrusion prevention system)
        - WEB/EMAIL security.

# Load Balancers
- Commonly used for managing packet distribution for an application access.
- There are multiple applications and we need to grant:
    - Good performance
    - Redundancy

# DHCP (Dynamic Host Configuration Protocol)
- Provide dynamic IP address to end hosts.
- Manage Pools and ranges from the server side.
- Assignments: leases with an expiration timer. On the time is expired the lease time is renewed.

## DHCP messages (DORA)
- **D:** Discover. This message is sent by the host to the server.
    - Host uses broadcast message and uses its own mac-address as SRC.
- **O:** Offer. This message is the server answer to the host.
- **R:** Request. This is host the answer to server offer. 
- **A:** Acknowledge. Then Server replies with an ACK message.

## DHCP Relay
- It is a special feature used when we have multiples hosts grouped by VLANs and we need those get a DCHP IP. And DHCP sever is another part of the nwetwork.

- The router or MLS switch is configured with DCHP relay to convert the broadcast messages to uncast packets towards the DHCP server.

# DNS (Domain Name System)
- Translates Names (domains) to an IP addresses.
- DNS server: Contains the mapping for all intranet and also internet.
## Messages
- DNS Request: Sends the domain with the FQDN
- DNS Response: Answers with the IP address, Then the computer or router will know how to reach the destination IP.

## DNS hierarchy
1. Corporate DNS server
2. ISP DNS server
3. It sends to authorized server under .com or .net domain, etc.

# NAT (Network address translation)
- Configure a multiple private ip addresses to one public address 
## PAT (Port address translation)
- Add a source port (TCP/UDP) for each specific binding.
- This will be used to order the incoming messages and forward them to the mapped destination.
- This port can be custom. 
## SNAT (Static AT)
- Allows one to one configurations from public address to private address.
- Allows the block of some public addresses.


# SNMP (Simple network management protocol)
- Legacy way of automating things. 
- We can get info, set config and proactive alerting (SNMP Trap).

## Framework
- SNMP manager
    - Software manager server (NMS =  Network Management Server)
- SNMP agent
    - Network device

## SNMP Versions
- v2c: Plaintext string (community)
- v3: It has all needed with security. 
    - Integrity
    - Authentication
    - Encryption.

# NTP (Network Time Protocol)
- Allows time and date synchronization.
- **Stratum**: Are the levels
    - 1 to 15
    - 0 belongs to atomic clock
    - 1 is the highest value of synchronization
    - 15 lowest value of synchronization
- **Peers**:
    - NTP server IP
    - When there are multiple servers those can be used as active and standby.
- **Security**:
    - Time and synchronization is important.
    - ACL
    - Encryption and authentication.
