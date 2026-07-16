import json
import requests
from requests.auth import HTTPBasicAuth


HOST = "192.168.160.132"
PORT = 443  # default HTTPS port
USERNAME = "admin"
PASSWORD = "password"

# IOS XE RESTCONF base URL
BASE_URL = f"https://{HOST}:{PORT}/restconf"

# IETF operational interfaces (for status/up/down)
IETF_INTERFACES_STATE_RESOURCE = "/data/ietf-interfaces:interfaces-state"

# Cisco operational model with more detailed interface info (including IPs)
# YANG module: Cisco-IOS-XE-interfaces-oper:interfaces
CISCO_INTERFACES_OPER_RESOURCE = "/data/Cisco-IOS-XE-interfaces-oper:interfaces"

# Common headers for RESTCONF using JSON
HEADERS = {
  "Accept": "application/yang-data+json",
  "Content-Type": "application/yang-data+json",
}


def get_ietf_interfaces_state():
  """Retrieve interface operational state from the IETF model."""
  url = BASE_URL + IETF_INTERFACES_STATE_RESOURCE
  response = requests.get(
    url,
    auth=HTTPBasicAuth(USERNAME, PASSWORD),
    headers=HEADERS,
    verify=False,  # disable TLS verification for lab use; not for production
    timeout=30,
  )
  response.raise_for_status()
  return response.json()


def get_cisco_interfaces_oper():
  """Retrieve interface operational details from the Cisco IOS XE model."""
  url = BASE_URL + CISCO_INTERFACES_OPER_RESOURCE
  response = requests.get(
    url,
    auth=HTTPBasicAuth(USERNAME, PASSWORD),
    headers=HEADERS,
    verify=False,
    timeout=30,
  )
  response.raise_for_status()
  return response.json()


def build_ip_map_from_cisco_oper(data: dict) -> dict[str, str]:
  """
  Build a mapping {interface_name: "ip/mask"} from Cisco operational data.
  """
  ip_map: dict[str, str] = {}

  if not isinstance(data, dict):
    return ip_map

  # Expected:
  # {
  #   "Cisco-IOS-XE-interfaces-oper:interfaces": {
  #     "interface": [ {...}, {...} ]
  #   }
  # }
  root = (
    data.get("Cisco-IOS-XE-interfaces-oper:interfaces")
    or data.get("interfaces")
    or {}
  )
  interfaces = root.get("interface", [])
  if not isinstance(interfaces, list):
    return ip_map

  for intf in interfaces:
    if not isinstance(intf, dict):
      continue

    name = intf.get("name")
    if not name:
      continue

    ipv4 = intf.get("ipv4") or intf.get("ietf-ip:ipv4") or {}

    # On some IOS-XE models, "ipv4" is just a string with the IP,
    # and the netmask/prefix is a separate field on the same interface.
    if isinstance(ipv4, str):
      ip = ipv4
      netmask = (
        intf.get("netmask")
        or intf.get("mask")
        or intf.get("prefix-length")
      )
      ip_display = f"{ip}/{netmask}" if netmask is not None else ip
      ip_map[name] = ip_display
      continue

    if not isinstance(ipv4, dict):
      continue

    addresses = ipv4.get("address") or ipv4.get("ietf-ip:address") or []
    if isinstance(addresses, dict):
      addresses = [addresses]
    if not isinstance(addresses, list) or not addresses:
      continue

    first_addr = addresses[0]
    if not isinstance(first_addr, dict):
      continue

    # Try common Cisco/IETF patterns for IPv4 address
    ip = first_addr.get("ip")
    netmask = first_addr.get("netmask") or first_addr.get("prefix-length")

    # Some Cisco models nest the primary address under "primary"
    if not ip:
      primary = first_addr.get("primary") or {}
      if isinstance(primary, dict):
        ip = primary.get("address") or primary.get("ip")
        netmask = primary.get("mask") or primary.get("netmask") or netmask

    if not ip:
      continue

    ip_display = f"{ip}/{netmask}" if netmask is not None else ip
    ip_map[name] = ip_display

  return ip_map


def print_interface_brief(ietf_data: dict, ip_map: dict[str, str] | None = None) -> None:
  """
  Print a summary similar to 'show ip interface brief'.

  Expected structure (IOS XE / ietf-interfaces):
  {
    "ietf-interfaces:interfaces-state": {
      "interface": [
        {
          "name": "...",
          "oper-status": "...",
          "admin-status": "...",
          "ipv4": {
            "address": [
              {"ip": "...", "netmask": "..."},
              ...
            ]
          }
        },
        ...
      ]
    }
  }
  """
  root = ietf_data.get("ietf-interfaces:interfaces-state", {})
  interfaces = root.get("interface", [])

  # Header similar to IOS XE
  header = f"{'Interface':<20}{'IP-Address/Mask':<22}{'OK?':<5}{'Method':<8}{'Status':<12}{'Protocol':<10}"
  print(header)
  print("-" * len(header))

  for intf in interfaces:
    name = intf.get("name", "")

    # Prefer IPs from Cisco operational model if available
    ip_display = "unassigned"
    if ip_map:
      ip_display = ip_map.get(name, "unassigned")

    # If Cisco model doesn't have an IP, fall back to whatever might be
    # present in the IETF interfaces-state tree.
    if ip_display == "unassigned":
      ipv4 = intf.get("ipv4") or intf.get("ietf-ip:ipv4") or {}
      addresses = (
        ipv4.get("address")
        or ipv4.get("ietf-ip:address")
        or []
      )

      if isinstance(addresses, list) and addresses:
        first_addr = addresses[0] or {}
        ip = first_addr.get("ip")
        netmask = first_addr.get("netmask") or first_addr.get("prefix-length")
        if ip:
          ip_display = f"{ip}/{netmask}" if netmask is not None else ip

    # There is no direct "OK?" or "Method" in the YANG model;
    # we just fill placeholders commonly seen on IOS XE.
    ok = "YES"
    method = "rest"

    status = intf.get("oper-status", "")
    protocol = "up" if status == "up" else "down"

    print(f"{name:<20}{ip_display:<22}{ok:<5}{method:<8}{status:<12}{protocol:<10}")


def main():
  # Disable insecure request warnings for lab environments
  requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
  )

  try:
    ietf_state = get_ietf_interfaces_state()
    cisco_oper = get_cisco_interfaces_oper()
    ip_map = build_ip_map_from_cisco_oper(cisco_oper)

    print("=== Interface Brief (RESTCONF / IETF + Cisco operational) ===")
    print_interface_brief(ietf_state, ip_map)
  except requests.HTTPError as http_err:
    print(f"HTTP error: {http_err} - body: {http_err.response.text}")
  except Exception as exc:
    print(f"Failed to retrieve interface data: {exc}")


if __name__ == "__main__":
  main()

