#!/usr/bin/env python3

from fmcapi import *
import json
import sys
import os
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

def _fmc_host(url_or_host: str) -> str:
    s = url_or_host.strip().rstrip("/")
    if "://" in s:
        u = urlparse(s)
        if u.netloc:
            return u.netloc
        return s.split("://", 1)[-1].split("/")[0]
    return s

def _env(name: str) -> str:
    v = os.getenv(name)
    if v is None or not str(v).strip():
        raise ValueError(f"Missing required environment variable: {name}")
    return str(v).strip()


def _truthy_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    raw = raw.strip().lower()
    if raw in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if raw in {"0", "false", "f", "no", "n", "off"}:
        return False
    raise ValueError(f"Invalid value for {name}: {raw!r} (expected true/false)")

def _int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return int(raw.strip())


def main():
    # FMC API credentials
    # host = "fmcrestapisandbox.cisco.com"
    # username = "knoxkn"
    # password = "q82ou&_XgM&21mbE"

    try:
        host = _fmc_host(_env("FMC_URL"))
        username = _env("FMC_USERNAME")
        password = _env("FMC_PASSWORD")
        verify = _truthy_env("FMC_VERIFY_SSL", True)
        timeout_s = _int_env("FMC_TIMEOUT_S", 60)
        domain_name = os.getenv("FMC_DOMAIN")
        domain_name = domain_name.strip() if domain_name else None
        domain_uuid_override = os.getenv("FMC_DOMAIN_UUID")
        domain_uuid_override = domain_uuid_override.strip() if domain_uuid_override else None
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

    try:
        # Create FMC connection object
        with FMC(
            host=host,
            username=username,
            password=password,
            autodeploy=False,
            file_logging=False
        ) as fmc:
            print("Successfully connected to FMC!")

            # Get devices
            print("\nFetching devices...")
            devices = DeviceRecords(fmc=fmc)
            device_list = devices.get()
            if device_list:
                print("\nDevices:")
                print(json.dumps(device_list, indent=2))

            # Get access policies
            print("\nFetching access policies...")
            access_policies = AccessPolicies(fmc=fmc)
            policy_list = access_policies.get()
            if policy_list:
                print("\nAccess Policies:")
                print(json.dumps(policy_list, indent=2))

            # Get network objects
            print("\nFetching network objects...")
            networks = Networks(fmc=fmc)
            network_list = networks.get()
            if network_list:
                print("\nNetwork Objects:")
                print(json.dumps(network_list, indent=2))

            # Get security zones
            print("\nFetching security zones...")
            zones = SecurityZones(fmc=fmc)
            zone_list = zones.get()
            if zone_list:
                print("\nSecurity Zones:")
                print(json.dumps(zone_list, indent=2))

            # Get interface groups
            print("\nFetching interface groups...")
            interface_groups = InterfaceGroups(fmc=fmc)
            group_list = interface_groups.get()
            if group_list:
                print("\nInterface Groups:")
                print(json.dumps(group_list, indent=2))

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 