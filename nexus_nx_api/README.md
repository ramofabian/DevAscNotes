# Automation Nexus devices with NX-API
Notes:
- Nexus devices runs an OS called NX-OS which is a fork of a linux.
- NX-OS uses the `features` in the same way as `systemctl` in linux to enable/disable services.
- One service inside is NXAPI which we need to turn on:
    - CLI -> Sandbox
    - REST -> Visore -> web server in nginx

## How to configure an IP address for MGMT and enable NXAPI feature
1. We need to enable a feature:
```sh
conf t
#Enable interface vlan feature
feature interface-vlan
#Enable DHCP feature
feature dhcp
end
```
2. Configure dhcp
```sh
conf t
interface mgmt0
ip add dhcp
no shut
end
```
3. Verification
```sh
show ip int brief vrf management
```
4. Enable `NXAIP`
```sh
conf t
feature nxapi
end
#Optional! -> save this config in the startup config
copy run start
```
## NXAPI
This is a web service with 3 services:
- NXAPI-CLI
- NXAPI-REST (DME)
- RESCONF (YANG)

### NXAPI-CLI
It sends request with  the entered CLI command and retrieves the output in json format.
Example:
1. Sending the command `show version`.
2. Request should be like:
```json
[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show version",
      "version": 1
    },
    "id": 1
  }
]
```
3. Node respose:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "body": {
      "header_str": "Cisco Nexus Operating System (NX-OS) Software\nTAC support: http://www.cisco.com/tac\nDocuments: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html\nCopyright (c) 2002-2020, Cisco Systems, Inc. All rights reserved.\nThe copyrights to certain works contained herein are owned by\nother third parties and are used and distributed under license.\nSome parts of this software are covered under the GNU Public\nLicense. A copy of the license is available at\nhttp://www.gnu.org/licenses/gpl.html.\n\nNexus 9000v is a demo version of the Nexus Operating System\n",
      "bios_ver_str": "",
      "kickstart_ver_str": "9.3(5)",
      "nxos_ver_str": "9.3(5)",
      "bios_cmpl_time": "",
      "kick_file_name": "bootflash:///nxos.9.3.5.bin",
      "nxos_file_name": "bootflash:///nxos.9.3.5.bin",
      "kick_cmpl_time": "7/20/2020 20:00:00",
      "nxos_cmpl_time": "7/20/2020 20:00:00",
      "kick_tmstmp": "07/20/2020 23:30:11",
      "nxos_tmstmp": "07/20/2020 23:30:11",
      "chassis_id": "Nexus9000 C9300v Chassis",
      "cpu_name": "Intel(R) Xeon(R) Gold 6148 CPU @ 2.40GHz",
      "memory": 8163456,
      "mem_type": "kB",
      "proc_board_id": "92I8ER456HS",
      "host_name": "n9k",
      "bootflash_size": 4287040,
      "kern_uptm_days": 0,
      "kern_uptm_hrs": 22,
      "kern_uptm_mins": 39,
      "kern_uptm_secs": 49,
      "rr_reason": "Unknown",
      "rr_sys_ver": "",
      "rr_service": "",
      "plugins": "Core Plugin, Ethernet Plugin",
      "manufacturer": "Cisco Systems, Inc.",
      "TABLE_package_list": {
        "ROW_package_list": {
          "package_id": "mtx-openconfig-all-1.0.0.0-9.3.5.lib32_n9000"
        }
      }
    }
  },
  "id": 1
}
```