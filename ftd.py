import requests
import json

url = 'https://10.10.20.65/api/fdm/v5/'
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}


def get_started():
    #Passwords taken from developer.cisco.com FTD lab
    data = json.dumps({"grant_type": "password", "username": "admin", "password": "Cisco1234"})
    token_start = requests.post(url + 'fdm/token', headers=headers, data=data, verify=False).json()
    token = token_start["access_token"]
    headers['Authorization'] = "Bearer " + token
    return headers

def get_secZones():
    headers = get_started()
    secZones = requests.get(url + 'object/securityzones', headers=headers, verify=False).json()
    return secZones

def secZone_table(secZones):
    print('Zone Name\t\tZone Interfaces')
    for z in secZones['items']:
        print(z['name'] + '\t\t' + z['interfaces'][0]['hardwareName'])

def getNTP():
    headers = get_started()
    ntp = requests.get(url + 'devicesettings/default/ntp', headers=headers, verify=False).json()
    print('NTP servers used:')
    print('-' * 40)
    for n in ntp['items'][0]['ntpServers']:
        print(n)

def getPolicies():
    headers = get_started()
    policies = requests.get(url + 'policy/accesspolicies', headers=headers, verify=False).json()
    parentId = policies['items'][0]['id']
    print(policies['items'][0]['name'] + ' ' + policies['items'][0]['id'])
    PolicyRules = requests.get(url + 'policy/accesspolicies/' + parentId + '/accessrules', headers=headers, verify = False).json()
    return PolicyRules

def printPolicyRules(rules):
    print('Rule Name\t\tSource Zone\t\tSource IP\t\tDest Zone\t\tDest IP\t\tDest Port\tAction')
    print('-' * 80)
    for r in rules['items']:
        name = r['name']
        sourceZones = r['sourceZones'][0]['name']
        sourceIP = r['sourceNetworks']
        destinationZones = r['destinationZones'][0]['name']
        destinationIP = r['destinationNetworks'][0]['name']
        destPort = r['destinationPorts'][0]['name']
        ruleAction = r['ruleAction']
        if sourceIP == []:
            sourceIP = 'ANY'
        if destinationIP == []:
            destinationIP = 'ANY'
        if destPort == []:
            destPort = 'ANY'
        print(name + '\t\t' + sourceZones + '\t\t' + sourceIP + '\t\t' + destinationZones + '\t\t' + destinationIP + '\t\t' + destPort +'\t' + ruleAction)

def get_network_objects():
    headers = get_started()
    response = requests.get(url + 'object/networks', headers=headers, verify=False).json()
    print('Object Name          Object Value')
    for r in response['items']:
        print(r['name'] + ' '*16 + r['value'])

def create_network_object():
    headers = get_started()
    name = input('Select a name for your object: ')
#    types = ['HOST', 'NETWORK', 'FQDN', 'RANGE']
#    while True:
#        subType = input('What type of object would you like ')
#        if subType not in types:
#            print('You must select:  HOST, NETWORK, FQDN, or RANGE')
#            pass
#        else:
#            break
    subType = "NETWORK"
    value = input('Input a value for your object:  ')
    type = "networkobject"
    data = json.dumps({"name": name,
                       "subType": subType,
                       "value": value,
                       "type": type})
    response = requests.post(url + 'object/networks', headers=headers, data=data, verify=False)
    if response.status_code == 200:
        print('Object created successfully')
    else:
        print('Something went wrong with your request')

def create_rule(parentId):
    headers = get_started()
    name = input('Name:  ')
    print('Your options are:')
    print('PERMIT        [1]')
    print('TRUST         [2]')
    print('DENY          [3]')
    ruleChoice = int(input('Make your choice: '))
    choices = {1: "PERMIT", 2: "TRUST", 3: "DENY"}
    ruleAction = choices[ruleChoice]
    data = json.dumps({
        "name": name,
        "ruleAction": ruleAction,
        "type": "accessrule"
    })
    response = requests.post(url + 'policy/accesspolicies/' + parentId + '/accessrules', headers=headers, data=data, verify=False)
    return response

def deploy_changes():
    headers = get_started()
    response = requests.post(url + 'operational/deploy', headers=headers, verify=False)
    return response

def get_int_policies():
    headers = get_started()
    response = requests.get(url + '/policy/intrusionpolicies', headers=headers, verify=False).json()
    return response

def get_int_rules():
    headers = get_started()
    response = requests.get(url + '/policy/intrusionpolicies', headers=headers, verify=False).json()
    print('Chose what policies rules you would like to view:')
    item = 0
    for r in response['items']:
        print(str(r['name']) + ' '*20 + '[' + str(item) + ']')
        item += 1
    choice = input('Pick the number for the appropriate policy:  ')
    parentId = response['items'][int(choice)]['id']
    response2 = requests.get(url + '/policy/intrusionpolicies/' + parentId + '/intrusionrules', headers=headers, verify=False).json()
    return response2