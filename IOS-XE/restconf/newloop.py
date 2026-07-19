import ipaddress
import os
from typing import Dict, Set

import requests
from requests.auth import HTTPBasicAuth


HOST = os.getenv("RESTCONF_HOST", "192.168.160.132")
PORT = int(os.getenv("RESTCONF_PORT", "443"))
USERNAME = os.getenv("RESTCONF_USER", "admin")
PASSWORD = os.getenv("RESTCONF_PASS", "password")

BASE_URL = f"https://{HOST}:{PORT}/restconf"

POOL = ipaddress.IPv4Network("20.20.20.0/24")
MASK = "255.255.255.255"

CISCO_INTERFACES_OPER_RESOURCE = "/data/Cisco-IOS-XE-interfaces-oper:interfaces"
LOOPBACK_CONFIG_RESOURCE = "/data/Cisco-IOS-XE-native:native/interface/Loopback"

HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}


def _restconf_get(resource: str) -> dict:
    url = BASE_URL + resource
    resp = requests.get(
        url,
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers=HEADERS,
        verify=False,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json() if resp.text else {}


def _restconf_put(resource: str, payload: dict) -> None:
    url = BASE_URL + resource
    resp = requests.put(
        url,
        json=payload,
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers=HEADERS,
        verify=False,
        timeout=30,
    )
    resp.raise_for_status()


def get_used_ips_in_pool() -> Set[ipaddress.IPv4Address]:
    """
    Return all IPs from POOL that are already in use on the device.
    """
    data = _restconf_get(CISCO_INTERFACES_OPER_RESOURCE)
    used: Set[ipaddress.IPv4Address] = set()

    root = (
        data.get("Cisco-IOS-XE-interfaces-oper:interfaces")
        or data.get("interfaces")
        or {}
    )
    interfaces = root.get("interface", [])
    if not isinstance(interfaces, list):
        return used

    for intf in interfaces:
        if not isinstance(intf, dict):
            continue

        ipv4 = intf.get("ipv4") or intf.get("ietf-ip:ipv4") or {}

        # Some models expose ipv4 as a simple string "ip/mask"
        if isinstance(ipv4, str):
            ip_str = ipv4.split("/")[0]
            try:
                ip = ipaddress.IPv4Address(ip_str)
            except ipaddress.AddressValueError:
                continue
            if ip in POOL:
                used.add(ip)
            continue

        if not isinstance(ipv4, dict):
            continue

        addresses = ipv4.get("address") or ipv4.get("ietf-ip:address") or []
        if isinstance(addresses, dict):
            addresses = [addresses]
        if not isinstance(addresses, list):
            continue

        for addr in addresses:
            if not isinstance(addr, dict):
                continue
            ip_str = addr.get("ip")
            if not ip_str:
                primary = addr.get("primary") or {}
                if isinstance(primary, dict):
                    ip_str = primary.get("address") or primary.get("ip")
            if not ip_str:
                continue
            try:
                ip = ipaddress.IPv4Address(ip_str)
            except ipaddress.AddressValueError:
                continue
            if ip in POOL:
                used.add(ip)

    return used


def choose_free_ip_from_pool(used: Set[ipaddress.IPv4Address]) -> ipaddress.IPv4Address:
    """
    Pick the first available /32 from POOL that is not in 'used'.
    """
    for host in POOL.hosts():
        if host not in used:
            return host
    raise RuntimeError(f"No free IPs available in pool {POOL}")


def get_existing_loopback_ids() -> Set[str]:
    """
    Return all existing Loopback interface IDs from the config.
    """
    try:
        data = _restconf_get(LOOPBACK_CONFIG_RESOURCE)
    except requests.HTTPError as exc:
        # If the Loopback container does not exist yet, treat as empty.
        if exc.response is not None and exc.response.status_code == 404:
            return set()
        raise

    root = (
        data.get("Cisco-IOS-XE-native:Loopback")
        or data.get("Loopback")
        or []
    )

    if isinstance(root, dict):
        root = [root]
    if not isinstance(root, list):
        return set()

    ids: Set[str] = set()
    for lb in root:
        if not isinstance(lb, dict):
            continue
        name = lb.get("name")
        if name is None:
            continue
        ids.add(str(name))
    return ids


def choose_new_loopback_id(existing: Set[str]) -> str:
    """
    Choose the smallest positive integer Loopback ID that does not already exist.
    """
    i = 1
    while str(i) in existing:
        i += 1
    return str(i)


def build_loopback_payload(loop_id: str, ip: ipaddress.IPv4Address) -> Dict:
    """
    Build RESTCONF JSON payload for a single Loopback interface.
    """
    return {
        "Cisco-IOS-XE-native:Loopback": {
            "name": int(loop_id),
            "ip": {
                "address": {
                    "primary": {
                        "address": str(ip),
                        "mask": MASK,
                    }
                }
            },
        }
    }


def create_loopback(loop_id: str, ip: ipaddress.IPv4Address) -> None:
    """
    Create or update a specific Loopback using PUT on the keyed resource.
    """
    resource = f"/data/Cisco-IOS-XE-native:native/interface/Loopback={loop_id}"
    payload = build_loopback_payload(loop_id, ip)
    _restconf_put(resource, payload)


def main() -> None:
    # Disable insecure request warnings for lab / demo use
    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning
    )

    try:
        used_ips = get_used_ips_in_pool()
        new_ip = choose_free_ip_from_pool(used_ips)

        existing_ids = get_existing_loopback_ids()
        new_id = choose_new_loopback_id(existing_ids)

        create_loopback(new_id, new_ip)

        print(f"Created Loopback{new_id} with IP {new_ip}/{MASK}")
        print(f"Device: {HOST}:{PORT} (RESTCONF user {USERNAME})")
    except requests.HTTPError as http_err:
        body = http_err.response.text if http_err.response is not None else ""
        print(f"HTTP error: {http_err} - body: {body}")
    except Exception as exc:
        print(f"Failed to create new loopback: {exc}")


if __name__ == "__main__":
    main()

