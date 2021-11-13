import requests
import json
import base64
from getpass import getpass

username = input('Please provide your username:  ')
ise_ip = input('Input the IP address of your ISE server:  ')
url = 'https://' + ise_ip + ':9060'
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

def get_started():
    #build headers to be used
    password = getpass()
    uspw = username + ':' + password
    auth = base64.b64encode(uspw.encode('ascii')).decode()
    headers['Authorization'] = 'Basic ' + auth
    return headers

def get_users():
    headers = get_started()
    internalUsers = requests.get(url + '/ers/config/internaluser', headers=headers, verify=False)
    return internalUsers

def create_user(name, desc):
    headers = get_started()
    #creates an internal user with an initial password
    data= json.dumps({
        "InternalUser": {
        "name": name,
          "password": 'P@ssw0rd',
          "changePassword": True,
          "description": desc}
    }
    )
    createUser = requests.post(url + '/ers/config/internaluser', headers=headers, data=data, verify=False)
    return createUser

def get_endpoint():
    headers = get_started()
    response = requests.get(url + '/ers/config/endpoint', headers=headers, verify=False)
    return response

def create_endpoint(name, mac):
    headers = get_started()
    body = json.dumps({
        "ERSEndPoint":{
            "name": name,
            "mac": mac
            }
        })
    response = requests.post(url +'/ers/config/endpoint', headers=headers, data=body, verify=False)
    if response.status_code == 201:
        print('Your endpoint was successfully created!')
    else:
        print('Hmmmm something went wrong.')
