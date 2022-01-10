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


def get_vk_upload_server(access_token, group_id):
    params = {
        'group_id': group_id,
    }
    url = f'https://api.vk.com/method/photos.getWallUploadServer?{params}&access_token={access_token}&v=5.131'
    response = requests.get(url, params=params)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']
    return upload_url


def vk_save_image(upload_url, group_id):
    pass


def vk_post_images(access_token, group_id, comment):
    upload_url = get_vk_upload_server(access_token, group_id)
    with open('images/latency.png', 'rb') as file:
        files = {
            'file': file,
        }
        upload_response = requests.post(upload_url, files=files)
        upload_response.raise_for_status()
        upload_res = upload_response.json()
        photo = upload_res['photo']
        server = upload_res['server']
        photo_hash = upload_res['hash']
        save_params = {
            'group_id': group_id,
            'photo': photo,
            'server': server,
            'hash': photo_hash,
        }
        save_url = f'https://api.vk.com/method/photos.saveWallPhoto?{save_params}&access_token={access_token}&v=5.131'
        save_response = requests.post(save_url, params=save_params)
        save_response.raise_for_status()
        saved_image = save_response.json()['response'][0]
        owner_id = saved_image['owner_id']
        media_id = saved_image['id']
        post_params = {
            'owner_id': -210037951,
            'from_group': 1,
            'attachments': f'photo{owner_id}_{media_id}',
            'message': comment,
        }
        post_url = f'https://api.vk.com/method/wall.post?{post_params}&access_token={access_token}&v=5.131'
        post_response = requests.post(post_url, params=post_params)
        post_response.raise_for_status()
        pprint(post_response.json())

def main():
    load_dotenv()
    CLIENT_ID = os.getenv('vk_client_id')
    ACCESS_TOKEN = os.getenv('vk_access_token')
    GROUP_ID = os.getenv('vk_group_id')
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics = response.json()
    download_comics(comics['img'])
    comment = comics['alt']
    vk_post_images(ACCESS_TOKEN, GROUP_ID, comment)


if __name__ == '__main__':
    main()
