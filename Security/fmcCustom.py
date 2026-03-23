#!/usr/bin/env python3
"""Query Cisco Secure Firewall / Firepower Management Center (FMC) via REST API.

Secrets and connection settings are read from environment variables (optionally from a
``.env`` file if ``python-dotenv`` is installed in your virtual environment).

Required:
  FMC_URL          Base URL, e.g. https://fmc.example.com (port optional)
  FMC_USERNAME     FMC login username
  FMC_PASSWORD     FMC login password

Optional:
  FMC_DOMAIN_UUID  Domain UUID; if unset, the first domain from /info/domain is used
  FMC_VERIFY_SSL   "true" / "false" (default: true). Set false only for lab/self-signed.
  FMC_TIMEOUT_S    Request timeout in seconds (default: 60)

On HTTP 401, the client refreshes the access token (FMC allows a short chain of refreshes)
and retries once; if refresh is not possible it performs a full login again.

Example (PowerShell, after activating venv):

  $env:FMC_URL = "https://fmc.lab.local"
  $env:FMC_USERNAME = "admin"
  $env:FMC_PASSWORD = "your-secret"
  $env:FMC_VERIFY_SSL = "false"
  python fmcCustom.py
"""

from __future__ import annotations

import base64
import json
import os
import sys
from collections.abc import Mapping
from typing import Any

import requests
import urllib3

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def _env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not str(value).strip():
        raise ValueError(f"Missing required environment variable: {name}")
    return str(value).strip()


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


def _normalize_base_url(url: str) -> str:
    url = url.strip().rstrip("/")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def _header_ci(headers: Mapping[str, str], *names: str) -> str | None:
    lower = {k.lower(): v for k, v in headers.items()}
    for n in names:
        v = lower.get(n.lower())
        if v:
            return v
    return None


class FmcApiClient:
    """FMC REST session with token refresh and one retry on 401."""

    _MAX_REFRESHES_BEFORE_LOGIN = 3

    def __init__(
        self,
        session: requests.Session,
        base_url: str,
        username: str,
        password: str,
        timeout_s: int,
    ) -> None:
        self.session = session
        self.base_url = base_url
        self._username = username
        self._password = password
        self.timeout_s = timeout_s
        self._refresh_token: str | None = None
        self._refreshes_since_login = 0

    def _apply_auth_headers(self, resp: requests.Response) -> None:
        access = _header_ci(resp.headers, "X-auth-access-token", "x-auth-access-token")
        refresh = _header_ci(resp.headers, "X-auth-refresh-token", "x-auth-refresh-token")
        if access:
            self.session.headers["X-auth-access-token"] = access
        if refresh:
            self._refresh_token = refresh

    def login(self) -> None:
        url = f"{self.base_url}/api/fmc_platform/v1/auth/generatetoken"
        token_bytes = f"{self._username}:{self._password}".encode("utf-8")
        basic = base64.b64encode(token_bytes).decode("ascii")
        headers = {
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/json",
        }
        resp = self.session.post(url, headers=headers, json={}, timeout=self.timeout_s)
        resp.raise_for_status()
        self._apply_auth_headers(resp)
        access = self.session.headers.get("X-auth-access-token")
        if not access:
            raise RuntimeError(
                "Authentication succeeded but no X-auth-access-token in response headers."
            )
        self._refreshes_since_login = 0

    def refresh(self) -> None:
        if self._refreshes_since_login >= self._MAX_REFRESHES_BEFORE_LOGIN:
            self.login()
            return
        if not self._refresh_token:
            self.login()
            return
        access = self.session.headers.get("X-auth-access-token")
        if not access:
            self.login()
            return
        url = f"{self.base_url}/api/fmc_platform/v1/auth/refreshtoken"
        headers = {
            "Content-Type": "application/json",
            "X-auth-access-token": access,
            "X-auth-refresh-token": self._refresh_token,
        }
        resp = self.session.post(url, headers=headers, json={}, timeout=self.timeout_s)
        resp.raise_for_status()
        self._apply_auth_headers(resp)
        if not self.session.headers.get("X-auth-access-token"):
            raise RuntimeError("Token refresh returned no X-auth-access-token.")
        self._refreshes_since_login += 1

    def _reauthenticate(self) -> None:
        try:
            if (
                self._refresh_token
                and self._refreshes_since_login < self._MAX_REFRESHES_BEFORE_LOGIN
            ):
                self.refresh()
                return
        except requests.HTTPError:
            pass
        self.login()

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout_s)
        resp = self.session.get(url, **kwargs)
        if resp.status_code == 401:
            self._reauthenticate()
            resp = self.session.get(url, **kwargs)
        resp.raise_for_status()
        return resp


def resolve_domain_uuid(client: FmcApiClient) -> str:
    explicit = os.getenv("FMC_DOMAIN_UUID")
    if explicit and explicit.strip():
        return explicit.strip()

    url = f"{client.base_url}/api/fmc_platform/v1/info/domain"
    resp = client.get(url)
    payload = resp.json()
    items = payload.get("items")
    if not isinstance(items, list) or not items:
        raise RuntimeError("No domains returned from /api/fmc_platform/v1/info/domain")
    first = items[0]
    if not isinstance(first, dict):
        raise RuntimeError("Unexpected domain list entry shape.")
    uuid = first.get("uuid")
    if not uuid:
        raise RuntimeError("Domain entry missing uuid.")
    return str(uuid)


def _paged_items(
    client: FmcApiClient, url: str, extra_params: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    offset = 0
    limit = 1000
    while True:
        params: dict[str, Any] = {"offset": offset, "limit": limit}
        if extra_params:
            params.update(extra_params)
        resp = client.get(url, params=params)
        data = resp.json()
        items = data.get("items")
        if not isinstance(items, list):
            raise RuntimeError(f"Unexpected JSON for {url}: missing 'items' list.")
        for it in items:
            if isinstance(it, dict):
                out.append(it)
        if len(items) < limit:
            break
        offset += limit
    return out


def get_device_records(client: FmcApiClient, domain_uuid: str) -> list[dict[str, Any]]:
    url = f"{client.base_url}/api/fmc_config/v1/domain/{domain_uuid}/devices/devicerecords"
    return _paged_items(client, url, {"expanded": "true"})


def get_deployable_devices(client: FmcApiClient, domain_uuid: str) -> list[dict[str, Any]]:
    url = f"{client.base_url}/api/fmc_config/v1/domain/{domain_uuid}/deployment/deployabledevices"
    return _paged_items(client, url)


# Policy collection endpoints (list GET). Some may 404 on older FMC builds; those are skipped.
POLICY_ENDPOINTS: tuple[tuple[str, str], ...] = (
    ("Access", "policy/accesspolicies"),
    ("Prefilter", "policy/prefilterpolicies"),
    ("FTD NAT", "policy/ftdnatpolicies"),
    ("Intrusion", "policy/intrusionpolicies"),
    ("File", "policy/filepolicies"),
    ("DNS", "policy/dnspolicies"),
    ("IKEv1", "policy/ikev1policies"),
    ("IKEv2", "policy/ikev2policies"),
)


def fetch_policies_by_type(client: FmcApiClient, domain_uuid: str) -> dict[str, list[dict[str, Any]]]:
    base = f"{client.base_url}/api/fmc_config/v1/domain/{domain_uuid}"
    result: dict[str, list[dict[str, Any]]] = {}
    for label, path in POLICY_ENDPOINTS:
        url = f"{base}/{path}"
        try:
            result[label] = _paged_items(client, url)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                result[label] = []
            else:
                raise
    return result


def _device_line(rec: dict[str, Any]) -> str:
    name = rec.get("name") or rec.get("hostName") or "(no name)"
    rid = rec.get("id") or rec.get("uuid") or "?"
    dtype = rec.get("type") or rec.get("deviceType") or ""
    host = rec.get("hostName") or rec.get("ipv4Address") or ""
    parts = [f"{name}", f"id={rid}"]
    if dtype:
        parts.append(f"type={dtype}")
    if host and str(host) != str(name):
        parts.append(f"host={host}")
    return " | ".join(parts)


def _print_section(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


def main() -> int:
    try:
        base_url = _normalize_base_url(_env("FMC_URL"))
        username = _env("FMC_USERNAME")
        password = _env("FMC_PASSWORD")
        verify = _truthy_env("FMC_VERIFY_SSL", True)
        timeout_s = _int_env("FMC_TIMEOUT_S", 60)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

    session = requests.Session()
    session.verify = verify
    if not verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    client = FmcApiClient(session, base_url, username, password, timeout_s)

    try:
        client.login()
        domain_uuid = resolve_domain_uuid(client)
    except (requests.RequestException, RuntimeError, ValueError) as e:
        print(f"FMC authentication or domain resolution failed: {e}", file=sys.stderr)
        return 1

    print(f"Connected to {base_url}")
    print(f"Using domain UUID: {domain_uuid}")

    try:
        devices = get_device_records(client, domain_uuid)
        _print_section(f"Devices ({len(devices)})")
        if not devices:
            print("(none)")
        else:
            for rec in devices:
                print(_device_line(rec))

        deployable = get_deployable_devices(client, domain_uuid)
        _print_section(f"Deployable devices ({len(deployable)})")
        if not deployable:
            print("(none — nothing pending deployment, or list empty)")
        else:
            for rec in deployable:
                print(_device_line(rec))

        policies = fetch_policies_by_type(client, domain_uuid)
        _print_section("Policies by type")
        total = 0
        for ptype, items in policies.items():
            total += len(items)
            print(f"\n{ptype} ({len(items)})")
            if not items:
                print("  (none)")
            else:
                for p in items:
                    name = p.get("name", "(no name)")
                    pid = p.get("id") or p.get("uuid") or "?"
                    print(f"  - {name}  [id={pid}]")
        print()
        print(f"Total policy objects listed: {total}")

        if os.getenv("FMC_JSON_DUMP"):
            _print_section("Raw JSON (FMC_JSON_DUMP set)")
            print(
                json.dumps(
                    {"devices": devices, "deployableDevices": deployable, "policies": policies},
                    indent=2,
                )
            )

    except requests.HTTPError as e:
        msg = e.response.text[:500] if e.response is not None else ""
        print(f"HTTP error: {e} {msg}", file=sys.stderr)
        return 1
    except (requests.RequestException, RuntimeError, ValueError) as e:
        print(f"Request failed: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
