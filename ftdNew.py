# Created while studying for Cisco's DEVCOR 350-901 Exam
# tokenStart username and password is configured for the FTD sandbox as of 28 May 2022

import requests
import json

url = 'https://10.10.20.65/api/fdm/latest/'

tokenStart = {
"grant_type": "password",
"username": "admin",
"password": "Sbxftd1234!"
}

def tokenGet():
    tokenGet = requests.post(url + 'fdm/token', json=tokenStart, verify=False)
    access_token = tokenGet.json()['access_token']
    headers = {'Authorization': 'Bearer ' + access_token}
    return headers

def networkObjectsGet(headers):
    netObjs = requests.get(url + 'object/networks', headers=headers, verify=False).json()
    return netObjs

def newObjectCreate(headers):
    while True:
        print('Please pick the object type you would like to create')
        print('Choose 1 for a Network Object')
        print('Choose 2 for a Host Object')
        print('Choose 3 for an FQDN object')
        print('Choose 4 for a range object')
        answer = int(input('Please select a number between 1 and 4:  '))
        if answer == 1:
            subtype = 'NETWORK'
            break
        elif answer == 2:
            subtype = 'HOST'
            break
        elif answer == 3:
            subtype = 'FQDN'
            break
        elif answer == 4:
            subtype = 'RANGE'
            break
        else:
            print('Please select a number between 1 and 4')
    name = input('Please select a name for your object: ')
    value = input('Please select a value for your object:  ')
    newObj = {
        "name": name,
        "subType": subtype,
        "value": value,
        "type": 'networkobject'
    }
    create = requests.post(url + 'object/networks', headers=headers, json=newObj, verify=False)
    if create.status_code != 200:
        print('Something went wrong, here is your error code')
        print(create.text)
    else:
        print('Network object created')

def networkObjectDelete(headers, id):
    delete = requests.delete(url + 'object/networks/' + id, headers=headers, verify=False)
    if delete.status_code != 204:
        print('Something went wrong, here is your error code')
        print(delete.text)
    else:
        print('Network object deleted')


def commitChanges(headers):
    response = requests.post(url + 'operational/deploy', headers=headers, verify=False)
    if response.status_code != 200:
        print('Here is your status code:  ' + response.json())
    else:
        print('Changes committed and deployed')

