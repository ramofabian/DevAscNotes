#!/usr/bin/env python3
"""
Connect to Cisco ISE using the `ciscoisesdk` library.

All private info (credentials) is read from environment variables (or an optional
local `.env` file via `python-dotenv`). Nothing sensitive is hard-coded.

Required (API Gateway mode):
  ISE_BASE_URL        Example: "https://198.18.133.27" (no trailing slash)
  ISE_USERNAME
  ISE_PASSWORD

Optional:
  ISE_API_VERSION     Default: "3.2_beta"
  ISE_USES_API_GATEWAY  Default: "true"
  ISE_USES_CSRF_TOKEN    Default: "false"
  ISE_VERIFY_SSL         Default: "true"  (set "false" for self-signed certs)
  ISE_SINGLE_REQUEST_TIMEOUT  Default: "60"
  ISE_WAIT_ON_RATE_LIMIT      Default: "true"
  ISE_DEBUG                    Default: "false"

Alternative auth (API Gateway mode):
  ISE_ENCODED_AUTH   Base64("username:password"), used instead of USERNAME/PASSWORD.

Notes:
- This script demonstrates a read-only API call: listing a few `network_device` items.
- If your ISE has API Gateway disabled, set `ISE_USES_API_GATEWAY=false` and also
  provide ERS/UI/MNT base URLs.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

import urllib3

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def _env(name: str) -> str:
    v = os.getenv(name)
    if v is None or not str(v).strip():
        raise ValueError(f"Missing required environment variable: {name}")
    return str(v).strip()


def _maybe_env(name: str) -> str | None:
    v = os.getenv(name)
    if v is None:
        return None
    if not str(v).strip():
        return None
    return str(v).strip()


def _truthy_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    s = str(raw).strip().lower()
    if s in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if s in {"0", "false", "f", "no", "n", "off"}:
        return False
    raise ValueError(f"Invalid boolean value for {name}: {raw!r}")


def _parse_verify(value: str | None, default: bool) -> bool | str:
    """
    ciscoisesdk's `verify` parameter supports either:
      - bool: verify TLS certs on/off
      - str: path to a CA bundle/cert
    """

    if value is None:
        return default
    raw = str(value).strip()
    if not raw:
        return default
    s = raw.lower()
    if s in {"0", "false", "f", "no", "n", "off"}:
        return False
    if s in {"1", "true", "t", "yes", "y", "on"}:
        return True
    # Treat anything else as a path (e.g. ".../ca-bundle.pem")
    return raw


def _normalize_base_url(url: str) -> str:
    url = url.strip().rstrip("/")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def build_ise_client() -> Any:
    """
    Create and return a `ciscoisesdk.IdentityServicesEngineAPI` client.
    """

    try:
        from ciscoisesdk import IdentityServicesEngineAPI
    except ImportError as e:
        raise RuntimeError(
            "Missing dependency `ciscoisesdk`. Install it with: pip install ciscoisesdk"
        ) from e

    uses_api_gateway = _truthy_env("ISE_USES_API_GATEWAY", True)
    uses_csrf_token = _truthy_env("ISE_USES_CSRF_TOKEN", False)

    version = os.getenv("ISE_API_VERSION", "3.2_beta").strip()
    timeout_s = int(os.getenv("ISE_SINGLE_REQUEST_TIMEOUT", "60"))
    wait_on_rate_limit = _truthy_env("ISE_WAIT_ON_RATE_LIMIT", True)
    debug = _truthy_env("ISE_DEBUG", False)

    verify = _parse_verify(os.getenv("ISE_VERIFY_SSL"), True)
    if verify is False:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    encoded_auth = _maybe_env("ISE_ENCODED_AUTH")

    if uses_api_gateway:
        base_url = _normalize_base_url(_env("ISE_BASE_URL"))

        if encoded_auth:
            return IdentityServicesEngineAPI(
                encoded_auth=encoded_auth,
                base_url=base_url,
                version=version,
                uses_api_gateway=True,
                uses_csrf_token=uses_csrf_token,
                verify=verify,
                single_request_timeout=timeout_s,
                wait_on_rate_limit=wait_on_rate_limit,
                debug=debug,
            )

        username = _env("ISE_USERNAME")
        password = _env("ISE_PASSWORD")
        return IdentityServicesEngineAPI(
            username=username,
            password=password,
            base_url=base_url,
            version=version,
            uses_api_gateway=True,
            uses_csrf_token=uses_csrf_token,
            verify=verify,
            single_request_timeout=timeout_s,
            wait_on_rate_limit=wait_on_rate_limit,
            debug=debug,
        )

    # API Gateway disabled: ciscoisesdk needs multiple base URLs.
    ers_base_url = _normalize_base_url(_env("ISE_ERS_BASE_URL"))
    ui_base_url = _normalize_base_url(_env("ISE_UI_BASE_URL"))
    mnt_base_url = _normalize_base_url(_env("ISE_MNT_BASE_URL"))
    px_grid_base_url = _normalize_base_url(_env("ISE_PX_GRID_BASE_URL"))

    if encoded_auth:
        return IdentityServicesEngineAPI(
            encoded_auth=encoded_auth,
            uses_api_gateway=False,
            uses_csrf_token=uses_csrf_token,
            ers_base_url=ers_base_url,
            ui_base_url=ui_base_url,
            mnt_base_url=mnt_base_url,
            px_grid_base_url=px_grid_base_url,
            version=version,
            verify=verify,
            single_request_timeout=timeout_s,
            wait_on_rate_limit=wait_on_rate_limit,
            debug=debug,
        )

    username = _env("ISE_USERNAME")
    password = _env("ISE_PASSWORD")
    return IdentityServicesEngineAPI(
        username=username,
        password=password,
        uses_api_gateway=False,
        uses_csrf_token=uses_csrf_token,
        ers_base_url=ers_base_url,
        ui_base_url=ui_base_url,
        mnt_base_url=mnt_base_url,
        px_grid_base_url=px_grid_base_url,
        version=version,
        verify=verify,
        single_request_timeout=timeout_s,
        wait_on_rate_limit=wait_on_rate_limit,
        debug=debug,
    )


def _print_network_devices(api: Any, page: int = 1, size: int = 5) -> None:
    """
    Read-only demo call: list a small page of network devices.
    """

    resp = api.network_device.get_all(page=page, size=size)
    resources = None

    # Typical shape from docs:
    # resp.response.SearchResult.resources -> list[dict]
    try:
        resources = resp.response.SearchResult.resources
    except Exception:
        # Fall back to returning whatever we got to avoid masking surprises.
        resources = getattr(getattr(resp, "response", None), "resources", None)

    if not resources:
        print("No network devices returned (or unexpected response shape).")
        if os.getenv("ISE_DEBUG"):
            print(json.dumps(resp, default=str, indent=2))
        return

    print(f"Network devices returned: {len(resources)}")
    for dev in resources:
        # Handle either dict-like or attribute-like objects.
        if isinstance(dev, dict):
            dev_id = dev.get("id")
            name = dev.get("name")
        else:
            dev_id = getattr(dev, "id", None)
            name = getattr(dev, "name", None)
        print(f"- {name or '(no name)'} (id={dev_id or 'unknown'})")


def main() -> int:
    try:
        api = build_ise_client()
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 2

    try:
        _print_network_devices(api)
    except Exception as e:
        # ciscoisesdk exceptions are not always importable if SDK versions drift,
        # so we keep this generic.
        print(f"ISE API call failed: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

