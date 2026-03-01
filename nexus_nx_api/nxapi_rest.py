import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from pprint import pprint

switchuser = 'admin'
switchpassword = 'RG!_Yw200'
switchip = '10.10.20.40'
cookies = {}

def get_token():
    auth_url = f'https://{switchip}/api/mo/aaaLogin.json'
    auth_body = {
        "aaaUser": {
            "attributes": {
                "name": switchuser,
                "pwd": switchpassword
                }
            }
        }
    try:
        auth_response = requests.post(
            auth_url, json=auth_body, timeout=5, verify=False)
        if auth_response.status_code == 200:
            auth_response_json = auth_response.json()
            if 'imdata' in auth_response_json.keys():
                token = auth_response_json['imdata'][0]['aaaLogin']['attributes']['token']
                cookies['APIC-Cookie'] = token
                return True
            else:
                raise ConnectionError(auth_response)
        else:
            raise ConnectionError(auth_response)
    except Exception as err:
        print(f"Error: {err}")
        return False

def get_all_physIface(all=True, iface:str=None):    
    headers = {"content-type": "application/json"}
    # Get the list of interfaces
    if all:
        interfaces_url = f'https://{switchip}/api/node/class/l1PhysIf.json?'
    else:
        interfaces_url = f'https://{switchip}/api/node/mo/sys/intf/phys-[{iface}].json?query-target=self'
    try:
        interfaces_response = requests.get(
            interfaces_url, headers=headers, cookies=cookies, verify=False)
        if interfaces_response.status_code == 200:
            return interfaces_response.json()
        else:
            raise ConnectionError(interfaces_response)
    except Exception as err:
        print(f"Error: {err}")
        return False

def create_loopback(name:str='lo123', description:str='Adding custom loopback'):
    headers = {"content-type": "application/json"}
    loopback_url = f'https://{switchip}/api/mo/sys/intf.json'
    loopback_body = {
        "interfaceEntity": {
            "children": [
              {
                "l3LbRtdIf": {
                  "attributes": {
                    "descr": description,
                    "id": name
                  }
                }
              }
            ]
        }
    }
    try:
        loopback_response = requests.post(
            loopback_url, headers=headers, cookies=cookies, verify=False, data=loopback_body)
        if loopback_response.status_code == 200 or loopback_response.status_code == 201:
            return loopback_response.json()
        else:
            raise ConnectionError(loopback_response)
    except Exception as err:
        print(f"Error: {err}")
        return False
def delete_loopback(name:str='lo123'):
    headers = {"content-type": "application/json"}
    loopback_url = f'https://{switchip}/api/mo/sys/intf/phys-[{name}].json'
    try:
        loopback_response = requests.delete(
            loopback_url, headers=headers, cookies=cookies, verify=False)
        if loopback_response.status_code == 200 or loopback_response.status_code == 204:
            return True
        else:
            raise ConnectionError(loopback_response)
    except Exception as err:
        print(f"Error: {err}")
        return False

def edit_port_description(iface:str, description:str):
    headers = {"content-type": "application/json"}
    port_url = f'https://{switchip}/api/mo/sys/intf/phys-[{iface}].json'
    port_body = {
        "l1PhysIf": {
            "attributes": {
                "descr": description
            }
        }
    }
    try:
        port_response = requests.put(
            port_url, headers=headers, cookies=cookies, verify=False, data=port_body)
        if port_response.status_code == 200 or port_response.status_code == 201:
            return port_response.json()
        else:
            raise ConnectionError(port_response)
    except Exception as err:
        print(f"Error: {err}")
        return False

def main():
    if get_token():
        print("Interfaces:","\n--------------------")
        pprint(get_all_physIface())
        print("Edit_port_description:","\n--------------------")
        edit_port_description(iface='eth1/1', description='Edited using REST API')
        pprint(get_all_physIface(all=False, iface='eth1/1'))
        print("Create_loopback:","\n--------------------")
        create_loopback()
        pprint(get_all_physIface(all=False, iface='lo123'))
        print("Delete_loopback:","\n--------------------")
        delete_loopback()
        pprint(get_all_physIface(all=False, iface='lo123'))