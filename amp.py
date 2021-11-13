import requests
import base64
import json

clientID = input('What is your client ID?  ')
apiKey = input('What is your API Key?  ')

url = 'https://' + clientID + ':' + apiKey + '@api.amp.cisco.com'
norm_url = 'https://api.amp.cisco.com'

def get_headers():
    auth = base64.b64encode((clientID + ':' + apiKey).encode('ascii')).decode()
    headers = {'Authorization': 'Basic ' + auth}
    return headers

def bas_policies():
    headers = get_headers()
    response = requests.get(norm_url + '/v1/policies', headers=headers)
    return response.json()

def get_policies():
    response = requests.get(url + '/v1/policies')
    return response

def get_computers():
    response = requests.get(url + '/v1/computers')
    return response

def get_events():
    response = requests.get(url + '/v1/events')
    return response

def compromise_count():
    response = requests.get(url + '/v1/computers').json()
    compromised = 0
    for r in response['data']:
        if r['is_compromised'] == True:
            compromised += 1
    print('There are currently ' + str(len(response['data'])) + ' computers on the network...\n'
        'and a total of ' + str(compromised) + ' are compromised!')

def get_comp_by_hostname(hostname):
    response = requests.get(url + '/v1/computers?hostname[]=' + hostname)
    return response

def get_policy_by_name(name):
    response = requests.get(url + '/v1/policies?name[]=' + name)
    return response