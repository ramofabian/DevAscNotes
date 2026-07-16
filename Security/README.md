# Cisco Security Platform APIs
## Cisco Products
- URL: https://www.cisco.com/site/us/en/products/security/index.html
### Firepower
- Same as firewall
- SDN solution (FMC) --> Controls all kinds of appliances Cisco has for firewalling.
- Controller uses API to controls all appliances.
- Cisco Secure Firewall Management Center [LINK](https://www.cisco.com/site/us/en/products/security/firewalls/firewall-management-center/index.html)
### XDR
- Extended Defense and Response system.
- It has an appliance to monitor all in the network and detecting anything that might be wrong.
- It works with other devices like:
    - Secure Endpoint (SE)
    - Secure Malware Analytics (SMA)
### Secure Endpoint (SE)
- Used to be installed on mobile devices (phones, tablets and laptops)
- Also called AMP for endpoints.
### Secure Malware Analytics (SMA)
- It used to be called threat grid.
- Sandbox environment
- When malware is detected or potentially identified it is sent to Threat grid where it actually inspects what this malware does by running it in an a sandbox enviroment and learns about what it is and what attacks.
### Umbrella
- It pushes policies onto devices
- It is at the end of its life
- Cisco Secure Access is the new product replacing it.
### Secure Connect
- It's an unified "all-in-one" solution designed to make SASE (Secure Access Service Edge) easy to deploy.
- It’s a cloud-based service that connects your employees (whether they are in a branch office or working from a coffee shop) to their apps and the internet, while wrapping everything in a layer of high-end security.
### ISE
- Identity Service Engine.
- It is a competitor of active directory.
- it can manage:
    - Users
    - Groups
    - Access and policies
- It can be integrated as authentication entity with others Cisco devices
## Cisco's Firewall Management Center (FMC) API
- API documentation: https://www.cisco.com/c/en/us/support/security/defense-center/products-programming-reference-guides-list.html
- We have to use basic authentication and in the header response the token is included and should be added for getting or posting requests.
- Additional links:
    - https://github.com/CiscoDevNet/fmc-rest-api/tree/master
    - https://github.com/marksull/fmcapi

### Python example: `fmcCustom.py`
Small script that authenticates to FMC, then prints registered devices, deployable devices (pending deployment), and policy objects (access, prefilter, NAT, intrusion, file, DNS, IKEv1/IKEv2). Credentials and URL are **not** hard-coded; they come from environment variables (or a local `.env` file if you use the optional dependency below).

**Install dependencies** (use a virtual environment first):

```bash
pip install -r requirements.txt
```

**Environment variables**

| Variable | Required | Description |
|----------|----------|-------------|
| `FMC_URL` | Yes | Base URL, e.g. `https://fmc.example.com` |
| `FMC_USERNAME` | Yes | FMC username |
| `FMC_PASSWORD` | Yes | FMC password |
| `FMC_DOMAIN_UUID` | No | Domain UUID; if omitted, the first domain from `/api/fmc_platform/v1/info/domain` is used |
| `FMC_VERIFY_SSL` | No | `true` or `false` (default `true`). Use `false` only for lab/self-signed certificates |
| `FMC_TIMEOUT_S` | No | HTTP timeout in seconds (default `60`) |
| `FMC_JSON_DUMP` | No | If set to any value, prints raw JSON for devices, deployable devices, and policies after the summary |

**Optional `.env` file:** If `python-dotenv` is installed (included in `requirements.txt`), create a `.env` in the same folder as the script with the variables above. **Do not commit `.env`** to git; it contains secrets.

**Run** (from the `Security` directory, after activating your venv):

```bash
export FMC_URL="https://your-fmc"
export FMC_USERNAME="admin"
export FMC_PASSWORD="your-secret"
python fmcCustom.py
```

On Windows PowerShell:

```powershell
$env:FMC_URL = "https://your-fmc"
$env:FMC_USERNAME = "admin"
$env:FMC_PASSWORD = "your-secret"
python fmcCustom.py
```
### Python example: `fmc_sdk.py` (FMC-API SDK)

Same information as `fmcCustom.py` (registered devices, deployable devices, policy summaries), but implemented with the **[fmcapi](https://pypi.org/project/fmcapi/)** package on PyPI. The SDK manages tokens and follows paging links; the script calls `fmcapi.FMC` and uses `send_to_api()` for the same REST paths as the raw `requests` client.

**Install dependencies** (includes `fmcapi`; use a virtual environment first):

```bash
pip install -r requirements.txt
```

Or install only the SDK:

```sh
pip install fmcapi
```

**Environment variables**

| Variable | Required | Description |
|----------|----------|-------------|
| `FMC_URL` | Yes | Base URL or hostname, e.g. `https://fmc.example.com` or `fmc.example.com` |
| `FMC_USERNAME` | Yes | FMC username |
| `FMC_PASSWORD` | Yes | FMC password |

**Optional `.env` file:** Same as for `fmcCustom.py`—if `python-dotenv` is installed, you can place variables in `.env` next to the script. **Do not commit `.env`** to git.

**Run** (from the `Security` directory, after activating your venv):

```bash
export FMC_URL="https://your-fmc"
export FMC_USERNAME="admin"
export FMC_PASSWORD="your-secret"
python fmc_sdk.py
```

On Windows PowerShell:

```powershell
$env:FMC_URL = "https://your-fmc"
$env:FMC_USERNAME = "admin"
$env:FMC_PASSWORD = "your-secret"
$env:FMC_VERIFY_SSL = "false"   # if using self-signed certs
python fmc_sdk.py
```

**Choosing `fmcCustom.py` vs `fmc_sdk.py`:** Use `fmcCustom.py` if you want a minimal dependency stack (`requests` only) and explicit control over auth headers. Use `fmc_sdk.py` if you prefer the maintained SDK for token handling and plan to extend the script with other `fmcapi` resource classes later.

## Cisco's ISE (Identity Service Engine)
- links:
    - API documentation: https://developer.cisco.com/docs/identity-services-engine/latest/
    - SDK documentation: https://ciscoisesdk.readthedocs.io/en/latest/
    - Devnet ISE: https://developer.cisco.com/identity-services-engine/
- Features:
    - Gather real-time contextual data for a network, including users and groups.
    - Gather network threats and vulnerabilities.
- **Important information**:
    - API should be turned on in 2 different places:
        - Enable API Gateway (this service receives requests through port 443)
        - Assign special privileges to user operating with API services:
            - Create an **ERS Admin** user (Full rights user)
            - Create an **ERS Operator** user (Read-only user)
    - API formats:
        - ERS API
        - Open API (More supported and used)
- Link to check Swagger documentation: `https://{ISE-IP/ISE-FQDN}/api/swagger-ui/index.html`
- Run python script `ise_api.py` to collect ise information.

## Python example: `ise_sdk.py` (Cisco ISE SDK - `ciscoisesdk`)

This script connects to Cisco ISE using the community SDK `ciscoisesdk` and makes a
small read-only call (lists a few `network_device` records).

All private information (credentials and connection settings) is read from environment
variables (no secrets are hard-coded in the script).

### Install dependencies

From the `Security` directory:

```bash
pip install -r requirements.txt
```

### Environment variables

API Gateway mode is enabled by default (`ISE_USES_API_GATEWAY=true`).

Required:

- `ISE_BASE_URL` (example: `https://198.18.133.27`)
- `ISE_USERNAME`
- `ISE_PASSWORD`

Optional:

- `ISE_API_VERSION` (default: `3.2_beta`)
- `ISE_VERIFY_SSL` (default: `true`; set `false` for lab/self-signed certs)
- `ISE_USES_API_GATEWAY` (default: `true`)
- `ISE_USES_CSRF_TOKEN` (default: `false`)
- `ISE_SINGLE_REQUEST_TIMEOUT` (default: `60`)
- `ISE_WAIT_ON_RATE_LIMIT` (default: `true`)
- `ISE_DEBUG` (default: `false`)
- `ISE_ENCODED_AUTH` (optional alternative to `ISE_USERNAME`/`ISE_PASSWORD`): Base64 of `username:password`

If your ISE API Gateway is disabled:

- Set `ISE_USES_API_GATEWAY=false`
- Also set:
  - `ISE_ERS_BASE_URL`
  - `ISE_UI_BASE_URL`
  - `ISE_MNT_BASE_URL`
  - `ISE_PX_GRID_BASE_URL`

### Run (PowerShell)

```powershell
$env:ISE_BASE_URL = "https://your-ise"
$env:ISE_USERNAME = "admin"
$env:ISE_PASSWORD = "your-secret"
$env:ISE_VERIFY_SSL = "false"   # if needed

python ise_sdk.py
```