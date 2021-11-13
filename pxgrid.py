import requests
import json
import base64
import time
from getpass import getpass

username = input('Enter your username:')
password = getpass()

headers = {"Accept-Language": "application/json", "Content-Type": "application/json"}

url = "https://10.10.6.49:8910/pxgrid/"

def get_started(name):
    print('This should only be used for new accounts')
    print('An administrator with access to the ISE GUI will have to approve your account during this function')
    body = json.dumps({
        "nodeName": name
    })
    accountCreate = requests.post(url + 'control/AccountCreate', headers=headers, data=body, verify=False).json()
    auth = base64.b64encode((name + ':' + accountCreate['password']).encode('ASCII')).decode()
    headers['Authorization'] = 'Basic ' + auth
    actBody = json.dumps({})
    accountActivate = requests.post(url + '/control/AccountActivate', headers=headers, data=actBody, verify=False).json()
    #no need to do anything with this...though maybe should do some error checking here?
    while True:
        time.sleep(5)
        accountCheck = requests.post(url + '/control/AccountActivate', headers=headers, data=actBody,
                                        verify=False).json()
        if accountCheck['accountState'] == 'PENDING':
            print(name + ' account is still PENDING')
        else:
            print('Your account has been enabled!')
            break
    secBody = json.dumps({"peerNodeName": "ise-admin-ise"})
    accessSecret = requests.post(url + '/control/AccessSecret', headers=headers, data=secBody, verify=False).json()
    secAuth = base64.b64encode((name + ':' + accessSecret['secret']).encode('ASCII')).decode()
    headers['Authorization'] = 'Basic ' + secAuth
    return headers

def create_headers():
    auth = base64.b64encode((username + ':' + password).encode('ASCII')).decode()
    headers['Authorization'] = 'Basic ' + auth
    return headers

def get_anc_endpoints():
    headers = create_headers()
    data = json.dumps({})
    response = requests.post(url + 'ise/config/anc/getEndpoints', headers=headers, data=data, verify=False).json()
    return response

def create_anc_endpoints(policyName, macAddress):
    headers = create_headers()
    body = json.dumps({"policyName": policyName,
                       "macAddress": macAddress})
    response = requests.post(url + 'ise/config/anc/applyEndpointByMacAddress', headers=headers, data=body, verify=False).json()
    return response