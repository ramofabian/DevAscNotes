import json
import os
from typing import Any, Dict, Optional

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError


class CatalystCenterClient:
    """
    Simple HTTP client for Cisco Catalyst Center (formerly DNAC)
    that handles authentication and reuses the auth token for
    subsequent requests.
    """

    def __init__(
        self,
        ip: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        ssl_verify: Optional[bool] = None,
    ) -> None:
        self.ip = ip or self._get_env_var("DNA_IP")
        self.username = username or self._get_env_var("DNA_USER")
        self.password = password or self._get_env_var("DNA_PASSWORD")
        self.base_url = f"https://{self.ip}"

        if ssl_verify is None:
            self.ssl_verify = self._get_ssl_verify_from_env()
        else:
            self.ssl_verify = ssl_verify

        self.session = requests.Session()
        self.session.verify = self.ssl_verify
        self._token: Optional[str] = None

    @staticmethod
    def _get_env_var(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise RuntimeError(f"Required environment variable '{name}' is not set.")
        return value

    @staticmethod
    def _get_ssl_verify_from_env() -> bool:
        """
        Interpret DNA_SSL as a boolean.
        Common "false" values: 0, false, no, off
        Anything else (or unset) is treated as True.
        """
        raw = os.getenv("DNA_SSL", "true").strip().lower()
        return raw not in {"0", "false", "no", "off"}

    def _build_url(self, path: str) -> str:
        if not path.startswith("/"):
            path = "/" + path
        return self.base_url + path

    def get_auth_token(self, force_refresh: bool = False) -> str:
        """
        Retrieve and cache an auth token from Cisco Catalyst Center.
        """
        if self._token is not None and not force_refresh:
            return self._token

        url = f"{self.base_url}/dna/system/api/v1/auth/token"

        try:
            response = self.session.post(
                url,
                auth=HTTPBasicAuth(self.username, self.password),
            )
            response.raise_for_status()
        except HTTPError as exc:
            raise RuntimeError(f"Failed to obtain token from {url}: {exc}") from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError("Auth response was not valid JSON.") from exc

        token = data.get("Token") or data.get("token")
        if not token:
            raise RuntimeError("Auth response JSON did not contain a 'Token' field.")

        self._token = token
        self.session.headers.update({"X-Auth-Token": self._token})
        return self._token

    def save_token_to_file(
        self,
        path: str = "tokenresponse.json",
        force_refresh: bool = False,
    ) -> str:
        """
        Get the current token and save it into a JSON file that
        looks like the sample auth response.
        """
        token = self.get_auth_token(force_refresh=force_refresh)
        data = {"Token": token}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return path

    def request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Generic authenticated request.

        Example:
            resp = client.request("GET", "/dna/intent/api/v1/network-device")
        """
        self.get_auth_token()
        url = self._build_url(path)
        response = self.session.request(method=method.upper(), url=url, **kwargs)
        response.raise_for_status()
        return response

    # Convenience methods for common HTTP verbs

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(
        self,
        path: str,
        json_body: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        if json_body is not None:
            kwargs.setdefault("json", json_body)
        return self.request("POST", path, **kwargs)

    def put(
        self,
        path: str,
        json_body: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        if json_body is not None:
            kwargs.setdefault("json", json_body)
        return self.request("PUT", path, **kwargs)

    def patch(
        self,
        path: str,
        json_body: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        if json_body is not None:
            kwargs.setdefault("json", json_body)
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    def head(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("HEAD", path, **kwargs)

    def options(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("OPTIONS", path, **kwargs)


# Simple default client for quick use in small scripts
_default_client: Optional[CatalystCenterClient] = None


def get_default_client() -> CatalystCenterClient:
    global _default_client
    if _default_client is None:
        _default_client = CatalystCenterClient()
    return _default_client


def get_token(force_refresh: bool = False) -> str:
    """
    Shortcut: get a token using the default client.
    """
    return get_default_client().get_auth_token(force_refresh=force_refresh)


def save_token_to_file(
    path: str = "tokenresponse.json",
    force_refresh: bool = False,
) -> str:
    """
    Shortcut: save token using the default client.
    """
    return get_default_client().save_token_to_file(path=path, force_refresh=force_refresh)


def get(path: str, **kwargs: Any) -> requests.Response:
    return get_default_client().get(path, **kwargs)


def post(
    path: str,
    json_body: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> requests.Response:
    return get_default_client().post(path, json_body=json_body, **kwargs)


def put(
    path: str,
    json_body: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> requests.Response:
    return get_default_client().put(path, json_body=json_body, **kwargs)


def patch(
    path: str,
    json_body: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> requests.Response:
    return get_default_client().patch(path, json_body=json_body, **kwargs)


def delete(path: str, **kwargs: Any) -> requests.Response:
    return get_default_client().delete(path, **kwargs)


def head(path: str, **kwargs: Any) -> requests.Response:
    return get_default_client().head(path, **kwargs)


def options(path: str, **kwargs: Any) -> requests.Response:
    return get_default_client().options(path, **kwargs)


if __name__ == "__main__":
    client = CatalystCenterClient()
    token = client.get_auth_token()
    print("Obtained token of length:", len(token))
    save_path = client.save_token_to_file(path="tokenresponse.json")
    print(f"Token saved to {save_path}")

