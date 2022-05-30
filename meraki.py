# Sorry this is no longer satuo...onto devcor

import requests
import json

apiKey = 'somekey'
networkId = 'somenetid'
orgId = 'someorgid'
username = 'someusername'
password = 'somepass'
url = 'https://api.meraki.com/api/v1/'

headers = {
    'Accept': "application/json",
    'Content-Type': "application/json",
    'X-Cisco-Meraki-API-Key': apiKey
}


def getOrgs():
    response = requests.get(url + 'organizations', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.text


def getOrgNets():
    response = requests.get(url + 'organizations/' + orgId + '/networks', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.text


def getNet():
    response = requests.get(url + 'networks/' + networkId, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.text


def getNetDev():
    response = requests.get(url + 'networks/' + networkId + '/devices', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.text


# Dig into simplifying this arg
def getNetSsid(ssidNumber='null'):
    if ssidNumber!= 'null':
        response = requests.get(url + 'networks/' + networkId + '/wireless/ssids/' + str(ssidNumber), headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    else:
        response = requests.get(url + 'networks/' + networkId + '/wireless/ssids', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return response.text


def updateNetSsid(ssidNumber):
    name = input('What would you like the SSID name to be?  ')
    print('Would you like to enable or disable this network?')
    print('Please select:')
    print('[1] to enable this network')
    print('[2] to disable this network')
    while True:
        enabledQ = input('Please select your choice:  ')
        if enabledQ == str(1):
            enabled = True
            break
        if enabledQ == str(2):
            enabled = False
            break
        else:
            print('You must select either 1 or 2 for this prompt.')
    data = json.dumps({
        "name": name,
        "enabled": enabled
    })
    response = requests.put(url + 'networks/' + networkId + '/wireless/ssids/' + str(ssidNumber), headers=headers,
                            data=data)
    if response.status_code == 200:
        print('SSID updated')
        return response.json()
    else:
        return response.text

