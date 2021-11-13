import requests
import json

from datetime import datetime, timezone, timedelta

key = input('Input your key:  ')
secret = input('Input your secret:  ')
customerKey = input('Input your customer key:  ')
org = input('Input your organization code:  ')

auth_url = 'https://management.api.umbrella.com/auth/v2/oauth2/token'
report_url = 'https://reports.api.umbrella.com/v2/organizations/'
enforce_url = 'https://s-platform.api.opendns.com/1.0'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

def reports_get_started():
    authStart = requests.post(auth_url, auth=(key, secret)).json()
    headers['Authorization'] = 'Bearer ' + authStart['access_token']
    return headers

def dns_report():
    headers = reports_get_started()
    start = input('How many days history do you want?  ')
    response = requests.get(report_url + org + '/activity/dns?from=-' + start + 'days&to=now&limit=10', headers=headers).json()
    return response

def top_dest():
    headers = reports_get_started()
    start = input('How many days history do you want?  ')
    typeOpt = {1: 'dns', 2: 'firewall', 3: 'proxy'}
    print('Select your destination type:')
    print(typeOpt)
    type = int(input())
    params = {'from': '-' + start + 'days', 'to': 'now', 'limit': '10', 'offset': '0'}
    response = requests.get(report_url + org + '/top-destinations/' + str(typeOpt[type]), headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print('Something went wrong')
        print(response.text)

def top_files():
    headers = reports_get_started()
    start = input('How many days history do you want?  ')
    params = {'from': '-' + start + 'days', 'to': 'now', 'limit': '10', 'offset': '0'}
    response = requests.get(report_url + org + '/top-files', headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print('Something went wrong')
        print(response.text)

def top_identities():
    headers = reports_get_started()
    start = input('How many days history do you want?  ')
    params = {'from': '-' + start + 'days', 'to': 'now', 'limit': '10', 'offset': '0'}
    response = requests.get(report_url + org + '/top-identities', headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print('Something went wrong')
        print(response.text)

def get_enf_domains():
    params = {'customerKey': customerKey}
    response = requests.get(enforce_url + '/domains', headers=headers, params=params)
    return response.json()

def enforce_add():
    params = {'customerKey': customerKey}
    dstDomain = input('What Domain do you want blocked?  ')
    dstUrl = input('What URL do you want blocked?  ')
    data = json.dumps({
        'alertTime': datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.0Z"),
        'deviceId': 'ba6a59f4-e692-4724-ba36-c28132c761de',
        'deviceVersion': '13.7a',
        'dstDomain': dstDomain,
        'dstUrl': dstUrl,
        'eventTime': datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.0Z"),
        'protocolVersion': '1.0a',
        'providerName': 'Security Platform'
    })
    response = requests.post(enforce_url + '/events', headers=headers, params=params, data=data)
    return response

def enforce_remove():
    domain = input('What domain do you want removed?  ')
    domains = get_enf_domains()
    for d in domains['data']:
        if domain == d['name']:
            id = d['id']
    params = {'customerKey': customerKey, 'id': id}
    response = requests.delete(enforce_url + '/domains/' + str(id), headers=headers, params=params)
    return response
