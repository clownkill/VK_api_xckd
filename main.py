import os
from random import randint

import requests
from dotenv import load_dotenv


def download_comic(comic_url, comic_file_name):
    response = requests.get(comic_url)
    response.raise_for_status()
    with open(comic_file_name, 'wb') as file:
        file.write(response.content)


def get_comic(comic_num, comic_file_name):
    url = f'https://xkcd.com/{comic_num}/info.0.json'
    comic_response = requests.get(url)
    comic_response.raise_for_status()
    comic = comic_response.json()
    comic_url = comic['img']
    comment = comic['alt']
    download_comic(comic_url, comic_file_name)
    return comment


def get_random_comic_num():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    count = response.json()['num']
    return randint(0, count)


def check_api_error(response):
    if 'error' in response.json():
        error = response.json()['error']['error_msg']
        raise requests.exceptions.HTTPError(f'Ошибка при запросе к API: {error}')


def get_vk_upload_server(access_token, group_id):
    params = {
        'group_id': group_id,
        'access_token': access_token,
        'v': '5.131',
    }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_api_error(response)
    upload_url = response.json()['response']['upload_url']
    return upload_url


def get_vk_save_params(upload_url, comic_file_name):
    with open(f'{comic_file_name}', 'rb') as file:
        files = {
            'file': file,
        }
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    check_api_error(response)
    upload_results = response.json()
    photo = upload_results['photo']
    server = upload_results['server']
    photo_hash = upload_results['hash']
    return photo, server, photo_hash


def get_vk_img_params(access_token, group_id, photo, server, photo_hash):
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
    check_api_error(response)
    saved_image = response.json()['response'][0]
    owner_id = saved_image['owner_id']
    media_id = saved_image['id']
    return owner_id, media_id


def post_vk_image(access_token, group_id, comment, comic_file_name):
    upload_url = get_vk_upload_server(access_token, group_id)
    photo, server, photo_hash = get_vk_save_params(upload_url, comic_file_name)
    owner_id, media_id = get_vk_img_params(access_token, group_id, photo, server, photo_hash)
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
    check_api_error(response)


def main():
    load_dotenv()
    ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')
    GROUP_ID = int(os.getenv('VK_GROUP_ID'))
    comic_file_name = 'comic.png'
    comic_num = get_random_comic_num()
    try:
        comment = get_comic(comic_num, comic_file_name)
        post_vk_image(ACCESS_TOKEN, GROUP_ID, comment, comic_file_name)
    finally:
        os.remove(comic_file_name)


if __name__ == '__main__':
    main()
