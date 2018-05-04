import requests
import json
import webbrowser
from urllib.parse import urlsplit
import os


consumer_key = os.environ['POCKET_CONSUMER_KEY']
redirect_uri = 'https://www.google.com'


url = 'https://getpocket.com/v3/oauth/request'
payload = {
    'consumer_key': consumer_key,
    'redirect_uri': redirect_uri
}
headers = {
    'Host': 'getpocket.com',
    'Content-Type': 'application/json; charset=UTF-8',
    'X-Accept': 'application/json'
}
r = requests.post(url, json=payload, headers=headers)
code = r.json()['code']

url = 'https://getpocket.com/auth/authorize?request_token=' + code + '&redirect_uri=' + redirect_uri
r = requests.get(url)
webbrowser.open(r.url)

url = ' https://getpocket.com/v3/oauth/authorize'
payload = {
    'consumer_key': consumer_key,
    'code': code
}
r = requests.post(url, json=payload, headers=headers)
#print(r.json())

access_token = r.json()['access_token']
username = r.json()['username']

url = ' https://getpocket.com/v3/get'
payload = {
    'consumer_key': consumer_key,
    'access_token': access_token,
    'sort': 'newest',
    "detailType":"simple"
}
r = requests.post(url, json=payload, headers=headers)


def list_urls(domain):
    result = []
    for key, value in r.json()['list'].items():
        url = value['given_url']
        base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
        if domain in base_url:
            result.append(value['given_url'])

    return result


