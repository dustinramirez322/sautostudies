import requests
import json
from datetime import datetime, timedelta, timezone

#Username and password taken from developer.cisco.com sandbox
username = "admin"
password = "C1sco12345"
url = "https://10.10.20.60"
repv1 = '/sw-reporting/v1/'

headers= {'Content-Type': 'application/json', 'Accept': 'application/json'}

def get_started():
    login_request_data = {
        "username": username,
        "password": password
    }
    response = requests.post(url + '/token/v2/authenticate', data=login_request_data, verify=False)
    if response.status_code == 200:
        print('Authentication Successful!')
        return dict(response.cookies)
    else:
        print('Something went wrong, you received a status code of ' + str(response.status_code))

def get_tenant(cookie):
    response = requests.get(url + repv1 + 'tenants', cookies=cookie, verify=False)
    return response

def get_hourly_traffic(cookie, tenantId):
    response = requests.get(url + repv1 + 'tenants/' + tenantId + '/externalGeos/traffic/hourly', cookies=cookie, verify=False).json()
    return response

def get_top_ports(cookie, tenantId, hoursAgo):
    (k, v), = cookie.items()
    headers['Cookie'] = k + '=' + v
    startTime = (datetime.now(timezone.utc) - timedelta(hours = hoursAgo)).strftime("%Y-%m-%dT%H:%M:%S.000")
    endTime = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000")
    body= json.dumps({"startTime": startTime,
                      "endTime": endTime})
    query = requests.post(url + repv1 + 'tenants/' + tenantId + '/flow-reports/top-ports/queries', headers=headers, data=body, verify=False)
    try:
        queryJson = query.json()
        print('Your query was successful and is currently in a ' + queryJson['data']['status'] + ' status with a queryId of ' + queryJson['data']['queryId'])
        return queryJson
    except:
        pass
    else:
        print('Something went wrong with your request')
        print('Your request received a ' + str(query.status_code))

def get_query_status(cookie, tenantId, queryId):
    (k, v), = cookie.items()
    headers['Cookie'] = k + '=' + v
    status = requests.get(url + repv1 + 'tenants/' + tenantId + '/flow-reports/top-ports/queries/' + queryId, headers=headers, verify=False).json()
    print('queryId of ' + status['data']['queryId'] + ' is currently in a ' + status['data']['status'] + ' status')
    return status


