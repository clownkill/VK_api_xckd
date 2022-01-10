import os
from urllib.parse import urlsplit
from pprint import pprint

import requests
from dotenv import load_dotenv

def fetch_file_name(url):
    url_file_path = urlsplit(url).path
    file_name = os.path.split(url_file_path)[-1]
    return file_name


def download_comics(comics_url):
    file_path = 'images/'
    directory = os.path.dirname(file_path)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    response = requests.get(comics_url)
    response.raise_for_status()
    name = fetch_file_name(comics_url)
    with open(f'images/{name}', 'wb') as file:
        file.write(response.content)


def check_vk(client_id, access_token):
    api_version = '5.131'
    method = 'groups.get'
    params = {
        'user_id': 80317736,
    }
    url = f'https://api.vk.com/method/{method}?{params}&access_token={access_token}&v={api_version}'
    response = requests.get(url, params=params)
    response.raise_for_status()
    pprint(response.json())

def main():
    load_dotenv()
    CLIENT_ID = os.getenv('vk_client_id')
    ACCESS_TOKEN = os.getenv('vk_access_token')
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics = response.json()
    download_comics(comics['img'])
    print(comics['alt'])
    check_vk(CLIENT_ID, ACCESS_TOKEN)


if __name__ == '__main__':
    main()
