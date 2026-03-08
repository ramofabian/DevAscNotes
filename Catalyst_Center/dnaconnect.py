from Catalyst_Center.dna_custom_libs.dnahttp import get, save_token_to_file


def print_devices():
    """
    Fetch devices from Catalyst Center and print hostname + IP
    in a simple table on the CLI.
    """
    # Ensure we have a valid token (and optionally save it)
    save_token_to_file()

    resp = get("/dna/intent/api/v1/network-device")
    data = resp.json()

    # DNAC typically returns {"response": [ ...devices... ], ...}
    devices = data.get("response", data)
    if isinstance(devices, dict):
        devices = [devices]
    elif not isinstance(devices, list):
        devices = []

    if not devices:
        print("No devices returned from Cisco Catalyst Center.")
        return

    rows = []
    for d in devices:
        hostname = d.get("hostname") or d.get("name") or "<unknown>"

        # managementIpAddress is common; ipAddress is sometimes a list
        ip = d.get("managementIpAddress")
        if not ip:
            ip_list = d.get("ipAddress") or []
            if isinstance(ip_list, list) and ip_list:
                ip = ip_list[0]
        ip = ip or "<no-ip>"

        rows.append((hostname, ip))

    name_width = max(len("HOSTNAME"), *(len(r[0]) for r in rows))
    ip_width = max(len("IP ADDRESS"), *(len(r[1]) for r in rows))

    header = f"{'HOSTNAME'.ljust(name_width)}  {'IP ADDRESS'.ljust(ip_width)}"
    separator = f"{'-' * name_width}  {'-' * ip_width}"

    print(header)
    print(separator)
    for hostname, ip in rows:
        print(f"{hostname.ljust(name_width)}  {ip.ljust(ip_width)}")


if __name__ == "__main__":
    print_devices()