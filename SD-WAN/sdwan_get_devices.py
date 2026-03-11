#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from typing import Any, Iterable

import requests


def _env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise ValueError(f"Missing required environment variable: {name}")
    return value.strip()


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


def _normalize_base_url(url: str) -> str:
    url = url.strip().rstrip("/")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def login(session: requests.Session, base_url: str, username: str, password: str, timeout_s: int) -> None:
    url = f"{base_url}/j_security_check"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"j_username": username, "j_password": password}

    resp = session.post(url, headers=headers, data=data, timeout=timeout_s)
    resp.raise_for_status()

    # Successful auth: empty body. Failure often returns an HTML login page.
    if resp.text and "<html" in resp.text.lower():
        raise RuntimeError("Authentication failed (received HTML login page). Check credentials.")

    # Ensure vManage session cookie is present after login.
    jsessionid = session.cookies.get("JSESSIONID") or resp.cookies.get("JSESSIONID")
    if not jsessionid:
        raise RuntimeError(
            "Authentication did not yield a JSESSIONID cookie. "
            "Verify VMANAGE_URL is correct and reachable, and credentials are valid."
        )


def try_get_xsrf_token(session: requests.Session, base_url: str, timeout_s: int) -> str | None:
    url = f"{base_url}/dataservice/client/token"
    resp = session.get(url, timeout=timeout_s)
    if resp.status_code != 200:
        return None
    token = resp.text.strip()
    return token or None


def get_devices(session: requests.Session, base_url: str, timeout_s: int) -> list[dict[str, Any]]:
    url = f"{base_url}/dataservice/device"
    resp = session.get(url, timeout=timeout_s)
    resp.raise_for_status()
    payload = resp.json()
    data = payload.get("data")
    if not isinstance(data, list):
        raise RuntimeError("Unexpected response shape from /dataservice/device (missing 'data' list).")
    return [d for d in data if isinstance(d, dict)]


def get_alarms(session: requests.Session, base_url: str, timeout_s: int) -> list[dict[str, Any]]:
    """
    Get recent alarms. When called without a query parameter, vManage typically
    returns alarms for the last ~30 minutes by default.
    """
    url = f"{base_url}/dataservice/alarms"
    resp = session.get(url, timeout=timeout_s)
    resp.raise_for_status()
    payload = resp.json()
    data = payload.get("data")
    if not isinstance(data, list):
        raise RuntimeError("Unexpected response shape from /dataservice/alarms (missing 'data' list).")
    return [d for d in data if isinstance(d, dict)]


def _format_table(rows: list[dict[str, Any]], columns: list[tuple[str, str]]) -> str:
    def to_str(v: Any) -> str:
        if v is None:
            return ""
        if isinstance(v, (str, int, float, bool)):
            return str(v)
        return str(v)

    headers = [label for _, label in columns]
    matrix: list[list[str]] = []
    for r in rows:
        matrix.append([to_str(r.get(key, "")) for key, _ in columns])

    widths = [len(h) for h in headers]
    for row in matrix:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def fmt_row(values: Iterable[str]) -> str:
        return "  ".join(v.ljust(widths[i]) for i, v in enumerate(values))

    out = []
    out.append(fmt_row(headers))
    out.append(fmt_row(["-" * w for w in widths]))
    out.extend(fmt_row(r) for r in matrix)
    return "\n".join(out)


def _ms_to_utc_str(ms: Any) -> str:
    try:
        value = int(ms)
    except (TypeError, ValueError):
        return ""
    try:
        dt = datetime.fromtimestamp(value / 1000.0, tz=timezone.utc)
    except (OverflowError, OSError, ValueError):
        return ""
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Log in to Cisco SD-WAN vManage and print device inventory."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.getenv("SDWAN_TIMEOUT_S", "30")),
        help="HTTP timeout in seconds (default: SDWAN_TIMEOUT_S or 30).",
    )
    args = parser.parse_args()

    try:
        base_url = _normalize_base_url(_env("VMANAGE_URL"))
        username = _env("VMANAGE_USERNAME")
        password = _env("VMANAGE_PASSWORD")
        verify_ssl = _truthy_env("SDWAN_VERIFY_SSL", default=True)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    session = requests.Session()
    session.verify = verify_ssl

    try:
        login(session, base_url, username, password, timeout_s=args.timeout)
        token = try_get_xsrf_token(session, base_url, timeout_s=args.timeout)
        if token:
            session.headers.update({"X-XSRF-TOKEN": token})

        devices = get_devices(session, base_url, timeout_s=args.timeout)
        alarms = get_alarms(session, base_url, timeout_s=args.timeout)
    except requests.exceptions.SSLError as e:
        print(
            "ERROR: SSL verification failed. If this is a lab with a self-signed cert, set "
            "SDWAN_VERIFY_SSL=false and try again.\n"
            f"Details: {e}",
            file=sys.stderr,
        )
        return 3
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    columns = [
        ("host-name", "HOSTNAME"),
        ("system-ip", "SYSTEM_IP"),
        ("site-id", "SITE"),
        ("device-type", "TYPE"),
        ("reachability", "REACH"),
        ("status", "STATUS"),
        ("version", "VERSION"),
    ]
    print("=== Devices ===")
    print(_format_table(devices, columns))
    print(f"\nTotal devices: {len(devices)}")

    # Prepare a simplified view for alarms so the table is easy to read.
    alarm_rows: list[dict[str, Any]] = []
    for a in alarms:
        # Try to resolve a friendly hostname.
        host_name = a.get("host_name") or ""
        if not host_name:
            vsd = a.get("values_short_display") or []
            if isinstance(vsd, list) and vsd:
                first = vsd[0]
                if isinstance(first, dict):
                    host_name = first.get("host-name", "") or first.get("host_name", "") or host_name

        alarm_rows.append(
            {
                "severity": a.get("severity", ""),
                "rule_name_display": a.get("rule_name_display") or a.get("type", ""),
                "host_name": host_name,
                "system_ip": a.get("system_ip", ""),
                "entry_time_str": _ms_to_utc_str(a.get("entry_time")),
                "message": a.get("message", ""),
            }
        )

    alarm_columns = [
        ("severity", "SEVERITY"),
        ("rule_name_display", "ALARM"),
        ("host_name", "HOSTNAME"),
        ("system_ip", "SYSTEM_IP"),
        ("entry_time_str", "TIME (UTC)"),
        ("message", "MESSAGE"),
    ]

    print("\n=== Alarms (recent) ===")
    if alarm_rows:
        print(_format_table(alarm_rows, alarm_columns))
    else:
        print("No alarms returned.")
    print(f"\nTotal alarms: {len(alarm_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

