import os
from urllib.parse import urlsplit

import requests


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


def main():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics = response.json()
    download_comics(comics['img'])
    print(comics['alt'])


if __name__ == '__main__':
    main()
