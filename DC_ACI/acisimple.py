import os
import sys
from typing import List, Tuple

import requests
from requests import Session


APIC_HOST_ENV = "APIC_HOST"
APIC_USERNAME_ENV = "APIC_USERNAME"
APIC_PASSWORD_ENV = "APIC_PASSWORD"
APIC_SSL_VERIFY_ENV = "APIC_SSL_VERIFY"  # "true"/"false" to control TLS verification


def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Required environment variable '{name}' is not set. "
            f"Set it in your virtual environment before running this script."
        )
    return value


def get_bool_env_var(name: str, default: bool = False) -> bool:
    """
    Parse a boolean-like environment variable.

    Accepted true values: "1", "true", "yes", "y", "on" (case-insensitive)
    Accepted false values: "0", "false", "no", "n", "off" (case-insensitive)
    """
    value = os.getenv(name)
    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False

    raise RuntimeError(
        f"Environment variable '{name}' must be a boolean string "
        f"(true/false, yes/no, 1/0, on/off). Got: '{value}'"
    )


def create_apic_session() -> Tuple[Session, str]:
    """
    Create an authenticated session to Cisco APIC using environment variables.

    Expected environment variables:
    - APIC_HOST: e.g. https://apic.example.com
    - APIC_USERNAME: APIC username
    - APIC_PASSWORD: APIC password
    - APIC_SSL_VERIFY: "true" / "false" (optional, defaults to "false")
    """
    host = get_env_var(APIC_HOST_ENV)
    username = get_env_var(APIC_USERNAME_ENV)
    password = get_env_var(APIC_PASSWORD_ENV)

    # Basic validation on host format
    if not host.startswith("http://") and not host.startswith("https://"):
        host = f"https://{host}"

    session = requests.Session()
    ssl_verify = get_bool_env_var(APIC_SSL_VERIFY_ENV, default=False)
    session.verify = ssl_verify

    # Suppress only the single InsecureRequestWarning from urllib3 if verify=False
    if not ssl_verify:
        try:
            from urllib3.exceptions import InsecureRequestWarning
            import urllib3

            urllib3.disable_warnings(category=InsecureRequestWarning)
        except Exception:
            # If anything goes wrong importing, just continue; it's non-fatal.
            pass

    login_url = f"{host}/api/aaaLogin.json"
    payload = {
        "aaaUser": {
            "attributes": {
                "name": username,
                "pwd": password,
            }
        }
    }

    resp = session.post(login_url, json=payload, timeout=10)
    if not resp.ok:
        raise RuntimeError(
            f"Failed to authenticate to APIC at '{host}'. "
            f"Status: {resp.status_code}, Body: {resp.text}"
        )

    # Extract the APIC token from the login response and make
    # sure it will be sent on subsequent requests.
    try:
        data = resp.json()
        token = data["imdata"][0]["aaaLogin"]["attributes"]["token"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(
            f"Login succeeded but no token was found in response: {resp.text}"
        )

    # Add token so it is included in request headers (Cookie)
    session.headers.update({"Cookie": f"APIC-cookie={token}"})

    return session, token


def get_tenants(session: Session, host: str, token: str) -> List[str]:
    """
    Retrieve a list of tenant names (fvTenant objects) from APIC.
    """
    if not host.startswith("http://") and not host.startswith("https://"):
        host = f"https://{host}"

    url = f"{host}/api/class/fvTenant.json"
    # Explicitly include the APIC token in the headers for this GET request.
    resp = session.get(url, headers={"Cookie": f"APIC-cookie={token}"}, timeout=10)
    if not resp.ok:
        raise RuntimeError(
            f"Failed to retrieve tenants. "
            f"Status: {resp.status_code}, Body: {resp.text}"
        )

    data = resp.json()
    imdata = data.get("imdata", [])

    tenants: List[str] = []
    for item in imdata:
        fv_tenant = item.get("fvTenant", {})
        attrs = fv_tenant.get("attributes", {})
        name = attrs.get("name")
        if name:
            tenants.append(name)

    return tenants


def main() -> int:
    try:
        host = get_env_var(APIC_HOST_ENV)
        session, token = create_apic_session()
        tenants = get_tenants(session, host, token)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not tenants:
        print("No tenants found.")
        return 0

    print("Tenants on APIC:")
    for t in tenants:
        print(f"- {t}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

