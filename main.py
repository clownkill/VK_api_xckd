import os
from random import randint

import requests
from dotenv import load_dotenv


def get_comic(comic_num, comic_file_name):
    url = f'https://xkcd.com/{comic_num}/info.0.json'
    comic_response = requests.get(url)
    comic_response.raise_for_status()
    comic = comic_response.json()
    comic_url = comic['img']
    comment = comic['alt']
    response = requests.get(comic_url)
    response.raise_for_status()
    with open(f'{comic_file_name}', 'wb') as file:
        file.write(response.content)
    return comment


def get_comics_count():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    count = response.json()['num']
    return randint(0, count)


def get_vk_upload_server(access_token, group_id):
    params = {
        'group_id': group_id,
        'access_token': access_token,
        'v': '5.131',
    }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=params)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']
    return upload_url


def vk_upload_image(upload_url, comic_file_name):
    with open(f'{comic_file_name}', 'rb') as file:
        files = {
            'file': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        upload_results = response.json()
        photo = upload_results['photo']
        server = upload_results['server']
        photo_hash = upload_results['hash']
    return photo, server, photo_hash


def vk_save_image(access_token, group_id, photo, server, photo_hash):
    params = {
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': photo_hash,
        'access_token': access_token,
        'v': '5.131',
    }
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(url, params=params)
    response.raise_for_status()
    saved_images = response.json()['response'][0]
    owner_id = saved_images['owner_id']
    media_id = saved_images['id']
    return owner_id, media_id


def vk_post_images(access_token, group_id, comment, comic_file_name):
    upload_url = get_vk_upload_server(access_token, group_id)
    photo, server, photo_hash = vk_upload_image(upload_url, comic_file_name)
    owner_id, media_id = vk_save_image(access_token, group_id, photo, server, photo_hash)
    params = {
        'owner_id': -group_id,
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': comment,
        'access_token': access_token,
        'v': '5.131',
    }
    url = 'https://api.vk.com/method/wall.post'
    response = requests.post(url, params=params)
    response.raise_for_status()


def main():
    load_dotenv()
    ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')
    GROUP_ID = int(os.getenv('VK_GROUP_ID'))
    comic_file_name = 'comic.png'
    comic_num = get_comics_count()
    comment = get_comic(comic_num, comic_file_name)
    vk_post_images(ACCESS_TOKEN, GROUP_ID, comment, comic_file_name)
    os.remove(comic_file_name)


if __name__ == '__main__':
    main()
