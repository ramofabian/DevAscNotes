import os
import random
from ncclient import manager

SUBNET_HOSTS = ["10.10.10.1", "10.10.10.2"]
MASK = "255.255.255.255"


def get_netconf_connection(
    host: str,
    username: str,
    password: str,
    port: int = 830,
    timeout: int = 30,
) -> manager.Manager:
    return manager.connect(
        host=host,
        port=port,
        username=username,
        password=password,
        hostkey_verify=False,
        device_params={"name": "csr"},
        look_for_keys=False,
        allow_agent=False,
        timeout=timeout,
    )


def build_loopbacks_edit_payload(loop1_ip: str, loop2_ip: str) -> str:
    # Root must be <config> in NETCONF base namespace for edit-config
    return f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>1</name>
        <ip>
          <address>
            <primary>
              <address>{loop1_ip}</address>
              <mask>{MASK}</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
      <Loopback>
        <name>2</name>
        <ip>
          <address>
            <primary>
              <address>{loop2_ip}</address>
              <mask>{MASK}</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
""".strip()


def build_loopbacks_filter_body() -> str:
    # NOTE: No <filter> wrapper here; we pass ("subtree", body) to ncclient.
    return """
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
    <Loopback><name>1</name></Loopback>
    <Loopback><name>2</name></Loopback>
  </interface>
</native>
""".strip()


def main() -> None:
    device = {
        "host": os.getenv("NETCONF_HOST", "192.168.160.0"),
        "username": os.getenv("NETCONF_USER", "admin"),
        "password": os.getenv("NETCONF_PASS", "password"),
        "port": int(os.getenv("NETCONF_PORT", "830")),
    }

    ips = SUBNET_HOSTS[:]
    random.shuffle(ips)
    loop1_ip, loop2_ip = ips[0], ips[1]

    payload = build_loopbacks_edit_payload(loop1_ip, loop2_ip)

    with get_netconf_connection(**device) as m:
        resp = m.edit_config(target="running", config=payload)
        print(f"Loopback1 -> {loop1_ip}/{MASK}")
        print(f"Loopback2 -> {loop2_ip}/{MASK}")
        print(resp)

        # Verify in running config (this is where the filter goes)
        flt = ("subtree", build_loopbacks_filter_body())
        verify = m.get_config(source="running", filter=flt)
        print(verify.xml)


if __name__ == "__main__":
    main()