"""
Use dnacentersdk to authenticate to Catalyst Center via environment variables
and run multiple GET requests, printing results in a readable format.
"""
import json
import os
import sys

from dnacentersdk import DNACenterAPI


def get_api():
    """Build DNACenterAPI from environment variables."""
    base_url = os.environ.get("DNA_IP")
    username = os.environ.get("DNA_USER")
    password = os.environ.get("DNA_PASSWORD")
    ssl_raw = os.environ.get("DNA_SSL", "true").strip().lower()
    verify = ssl_raw not in ("false", "0", "no")

    if not base_url or not username or not password:
        missing = [
            n for n, v in [
                ("DNA_IP", base_url),
                ("DNA_USER", username),
                ("DNA_PASSWORD", password),
            ]
            if not v
        ]
        print("Missing required environment variables:", ", ".join(missing), file=sys.stderr)
        print("Example: set DNA_IP=10.10.20.80 & set DNA_USER=admin & set DNA_PASSWORD=...", file=sys.stderr)
        sys.exit(1)

    if not base_url.startswith("http"):
        base_url = f"https://{base_url}"

    return DNACenterAPI(
        base_url=base_url,
        username=username,
        password=password,
        verify=verify,
    )


def pretty_print(title: str, data) -> None:
    """Print a section title and JSON data with indentation."""
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    if data is None:
        print("  (no data)")
        return
    text = json.dumps(data, indent=2)
    print(text)
    print()


def main():
    api = get_api()

    # 1) Network devices
    try:
        devices = api.devices.get_device_list()
        pretty_print("Network devices", devices.get("response") if isinstance(devices, dict) else devices)
    except Exception as e:
        pretty_print("Network devices (error)", {"error": str(e)})

    # 2) Site list (sites hierarchy)
    try:
        sites = api.sites.get_site()
        pretty_print("Sites", sites.get("response") if isinstance(sites, dict) else sites)
    except Exception as e:
        pretty_print("Sites (error)", {"error": str(e)})

    # 3) Topology (optional – can be heavy)
    try:
        topology = api.topology.get_topology_details()
        pretty_print("Topology details", topology)
    except Exception as e:
        pretty_print("Topology (error)", {"error": str(e)})

    # 4) Network health summary
    try:
        health = api.clients.get_overall_network_health()
        pretty_print("Overall network health", health)
    except Exception as e:
        try:
            health = api.health.get_network_health()
            pretty_print("Network health", health)
        except Exception as e2:
            pretty_print("Network health (error)", {"error": str(e2)})


if __name__ == "__main__":
    main()
