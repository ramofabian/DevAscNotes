from pprint import pprint
import xmltodict
from ncclient import manager


def get_netconf_connection(
    host: str,
    username: str,
    password: str,
    port: int = 830,
    timeout: int = 30,
) -> manager.Manager:
    """
    Establish and return a NETCONF connection to an IOS-XE device.

    Adjust `host`, `username`, and `password` when calling this function.
    """
    return manager.connect(
        host=host,
        port=port,
        username=username,
        password=password,
        hostkey_verify=False,
        device_params={"name": "csr"},  # common for IOS-XE/CSR1000v
        look_for_keys=False,
        allow_agent=False,
        timeout=timeout,
    )


def build_interfaces_filter() -> str:
    """
    Build a NETCONF filter targeting IOS-XE interface operational data.

    This uses the Cisco IOS-XE interfaces operational YANG model:
    `Cisco-IOS-XE-interfaces-oper`.
    """
    return """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
        <interface>
          <name></name>
          <description></description>
          <interface-type></interface-type>
          <admin-status></admin-status>
          <oper-status></oper-status>
          <ip-address></ip-address>
          <subnet-mask></subnet-mask>
        </interface>
      </interfaces>
    </filter>
    """.strip()


def parse_show_ip_int_brief_like(reply_xml: str) -> list[dict]:
    """
    Parse NETCONF XML reply into a list of interface dicts.

    Output is shaped to resemble `show ip interface brief`:
    [
        {
            "name": "GigabitEthernet1",
            "ip_address": "192.0.2.1",
            "ok": "YES",
            "method": "NVRAM",
            "status": "up",
            "protocol": "up",
        },
        ...
    ]
    """
    data = xmltodict.parse(reply_xml)
    pprint(data)

    # Navigate to interfaces list (best‑effort; handles single/multi interface)
    interfaces = (
        data.get("rpc-reply", {})
        .get("data", {})
        .get("interfaces", {})
        .get("interface", [])
    )

    if isinstance(interfaces, dict):
        interfaces = [interfaces]

    result = []
    for intf in interfaces:
        name = intf.get("name", "")
        ip = intf.get("ip-address", "unassigned")
        status = intf.get("oper-status", "")
        admin_status = intf.get("admin-status", "")

        result.append(
            {
                "name": name,
                "ip_address": ip or "unassigned",
                "ok": "YES",  # NETCONF/YANG doesn't expose this directly; assume OK
                "method": "",  # left empty; can be populated if config model is queried
                "status": status,
                "protocol": admin_status,
            }
        )

    return result


def print_show_ip_int_brief_like(interfaces: list[dict]) -> None:
    """Print interface data in a `show ip interface brief`-like table."""
    header = f"{'Interface':<20}{'IP-Address':<18}{'OK?':<6}{'Method':<8}{'Status':<12}{'Protocol':<10}"
    print(header)
    print("-" * len(header))

    for intf in interfaces:
        print(
            f"{intf['name']:<20}"
            f"{intf['ip_address']:<18}"
            f"{intf['ok']:<6}"
            f"{intf['method']:<8}"
            f"{intf['status']:<12}"
            f"{intf['protocol']:<10}"
        )


def main() -> None:
    """
    Example usage.

    Update the `DEVICE` dictionary with your IOS-XE device details before running:

        pip install ncclient xmltodict
        python connc.py
    """
    DEVICE = {
        "host": "192.168.160.134",  # TODO: change to your device IP / hostname
        "username": "admin",   # TODO: change to your username
        "password": "password",   # TODO: change to your password
        "port": 830,
    }

    netconf_filter = build_interfaces_filter()

    with get_netconf_connection(**DEVICE) as m:
        reply = m.get(netconf_filter)
        print("NETCONF Reply XML:")
        pprint(reply.xml)
        print("\nParsed Interface Data:")
        interfaces = parse_show_ip_int_brief_like(reply.xml)
        print_show_ip_int_brief_like(interfaces)


if __name__ == "__main__":
    main()

