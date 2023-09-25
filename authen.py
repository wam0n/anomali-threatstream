import requests
import json
import info
import os

def authen(url, headers, data):
    r = requests.request('POST', url=url, data=data, headers=headers)
    return r

def call_api(endpoint, csrftoken, sessionid):
    info.get_headers['Cookie'] = f"csrftoken={csrftoken}; sessionid={sessionid}"
    r = requests.get(url=endpoint, headers=info.get_headers)
    return r

def write_file(filename, info):
    filepath = os.path.join('results', filename)
    print(f'[+] Writing file {filepath}')
    with open(filepath, 'w') as f:
        json.dump(info, f, indent=4)

if __name__ == '__main__':

    reqUrl = "https://optic.threatstream.com/api/v1/user/login/"

    response = authen(reqUrl, info.post_headers, json.dumps(info.credentials))
    print('[+] Authen Success')

    csrftoken = (response.headers['set-cookie']).split(';')[0].split('=')[-1]
    sessionid = (response.headers['set-cookie']).split(';')[6].split('=')[-1]

    endpoints = info.endpoints
    
    for ep in endpoints:
        print(f'[+] Getting info from {ep}')
        response = call_api(ep, csrftoken, sessionid)
        filename = ep.split('=')[-1] + '.json'
        write_file(filename, json.loads(response.text))
