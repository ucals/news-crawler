import requests
from time import sleep
import json
import webbrowser
from urllib.parse import urlsplit
import os
from pathlib import Path


def get_pocket_data(save=True):
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
    sleep(5)

    url = ' https://getpocket.com/v3/oauth/authorize'
    payload = {
        'consumer_key': consumer_key,
        'code': code
    }
    r = requests.post(url, json=payload, headers=headers)
    access_token = r.json()['access_token']

    url = ' https://getpocket.com/v3/get'
    payload = {
        'consumer_key': consumer_key,
        'access_token': access_token,
        'sort': 'newest',
        "detailType": "simple"
    }

    data = requests.post(url, json=payload, headers=headers).json()
    if save:
        filename = os.path.join(str(Path.home()), 'Downloads', 'pocket_data.json')
        with open(filename, 'w') as fp:
            json.dump(data, fp)

    return data


def get_domain_data(domain):
    result = []
    for key, value in get_pocket_data()['list'].items():
        url = value['given_url']
        base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
        if domain in base_url:
            result.append(value)

    return result


# should be deprecated
def list_urls(domain):
    result = []
    for key, value in get_pocket_data()['list'].items():
        url = value['given_url']
        base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
        if domain in base_url:
            result.append(value['given_url'])

    return result


