import requests
import base64
import json

#For use with FMC and Splunk Lab
url = 'https://10.10.20.40/api/'
username = 'admin'
password = 'Cisco1234'

# For use with FMC Lab
#url = 'https://fmcrestapisandbox.cisco.com/api/'
#username = input('Input your sandbox username:  ')
#password = input('Input your sandbox password:  ')

#Used with either lab
domain = 'e276abec-e0f2-11e3-8169-6d9ed49b625f'
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

def get_started():
    uspw = username + ':' + password
    auth = base64.b64encode(uspw.encode('ascii')).decode()
    headers['Authorization'] = 'Basic ' + auth
    response = requests.post(url + 'fmc_platform/v1/auth/generatetoken', headers=headers, verify=False)
    del headers['Authorization']
    headers['X-auth-access-token'] = response.headers['X-auth-access-token']
    headers['X-auth-refresh-token'] = response.headers['X-auth-refresh-token']
    return headers

def get_hosts(headers):
    response = requests.get(url + 'fmc_config/v1/domain/default/object/hosts', headers=headers, verify=False).json()
    return response

def get_certain_host(headers, objectId):
    response = requests.get(url + 'fmc_config/v1/domain/default/object/hosts/' + objectId, headers=headers, verify=False).json()
    return response

def del_host(headers, objectId):
    response = requests.delete(url + 'fmc_config/v1/domain/default/object/hosts/' + objectId, headers=headers, verify=False).json()
    try:
        if response['error']['severity'] == 'ERROR':
            response: str = 'Sorry that host does not seem to exist'
    finally:
        return response

def create_host(headers, hostname, IP, **kwargs):
    desc = kwargs.get('desc', None)
    data= json.dumps({"type": "Host",
          "name": hostname,
          "value": IP,
          "description": desc})
    response = requests.post(url + 'fmc_config/v1/domain/default/object/hosts', headers=headers, data=data, verify=False)
    return response

def get_policies(headers):
    response = requests.get(url + 'fmc_config/v1/domain/default/policy/accesspolicies', headers=headers, verify=False).json()
    return response

def get_rules(headers):
    containerInfo = requests.get(url + 'fmc_config/v1/domain/default/policy/accesspolicies', headers=headers, verify=False).json()
    containerUUID = containerInfo['items'][0]['id']
    response = requests.get(url + 'fmc_config/v1/domain/default/policy/accesspolicies/' + containerUUID + '/accessrules', headers=headers, verify=False).json()
    return response

def create_rule(headers, policyname, action):
    containerInfo = requests.get(url + 'fmc_config/v1/domain/default/policy/accesspolicies', headers=headers, verify=False).json()
    containerUUID = containerInfo['items'][0]['id']
    data= json.dumps({"type": "AccessPolicy",
          "name": policyname,
          "action": action
        })
    response = requests.post(url + 'fmc_config/v1/domain/default/policy/accesspolicies/' + containerUUID + '/accessrules', headers=headers, data=data, verify=False).json()
    return response

def get_networks(headers):
    response = requests.get(url + 'fmc_config/v1/domain/default/object/networks', headers=headers, verify=False).json()
    return response