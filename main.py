import requests
import json
import info
import os
import sys

def authen(url, headers, data):
    r = requests.request('POST', url=url, data=data, headers=headers)
    return r

def call_api(endpoint, csrftoken, sessionid):
    info.get_headers['Cookie'] = f"csrftoken={csrftoken}; sessionid={sessionid}"
    r = requests.get(url=endpoint, headers=info.get_headers)
    return r

def write_file(dir, filename, info):
    filepath = os.path.join(dir, filename)
    print(f'[+] Writing file {filepath}')
    with open(filepath, 'w') as f:
        json.dump(info, f, indent=4)

if __name__ == '__main__':
    
    if len(sys.argv) < 2 or (sys.argv[1] not in ['ip', 'domain']):
        raise SystemExit("Please provide at least 1 argument {ip|domain}")

    if sys.argv[1] == 'ip':
        endpoints = info.Ips
        dir = 'IPs'
    elif sys.argv[1] == 'domain':
        endpoints = info.domains
        dir = 'domains'
    
    reqUrl = "https://optic.threatstream.com/api/v1/user/login/"

    response = authen(reqUrl, info.post_headers, json.dumps(info.credentials))
    print('[+] Authen Success')

    csrftoken = (response.headers['set-cookie']).split(';')[0].split('=')[-1]
    sessionid = (response.headers['set-cookie']).split(';')[6].split('=')[-1]

    for ep in endpoints:
        print(f'[+] Getting info from {ep}')
        response = call_api(ep, csrftoken, sessionid)
        filename = ep.split('=')[-1] + '.json'
        write_file(dir, filename, json.loads(response.text))
