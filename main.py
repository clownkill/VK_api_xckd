import os
from random import randint

import requests
from dotenv import load_dotenv


def download_comic(url):
    comic_url = requests.get(url).json()['img']
    response = requests.get(comic_url)
    response.raise_for_status()
    with open('comic.png', 'wb') as file:
        file.write(response.content)


def get_comic_comment(url):
    response = requests.get(url)
    response.raise_for_status()
    comment = response.json()['alt']
    return comment


def get_vk_upload_server(access_token, group_id):
    params = {
        'group_id': group_id,
    }
    url = f'https://api.vk.com/method/photos.getWallUploadServer?access_token={access_token}&v=5.131'
    response = requests.get(url, params=params)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']
    return upload_url


def vk_upload_image(upload_url):
    with open('comic.png', 'rb') as file:
        files = {
            'file': file,
        }
        upload_response = requests.post(upload_url, files=files)
        upload_response.raise_for_status()
        upload_res = upload_response.json()
        photo = upload_res['photo']
        server = upload_res['server']
        photo_hash = upload_res['hash']
    return photo, server, photo_hash


def vk_save_image(access_token, group_id, photo, server, photo_hash):
    params = {
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': photo_hash,
    }
    save_url = f'https://api.vk.com/method/photos.saveWallPhoto?access_token={access_token}&v=5.131'
    save_response = requests.post(save_url, params=params)
    save_response.raise_for_status()
    saved_image = save_response.json()['response'][0]
    owner_id = saved_image['owner_id']
    media_id = saved_image['id']
    return owner_id, media_id


def vk_post_images(access_token, group_id, comment):
    upload_url = get_vk_upload_server(access_token, group_id)
    photo, server, photo_hash = vk_upload_image(upload_url)
    owner_id, media_id = vk_save_image(access_token, group_id, photo, server, photo_hash)
    post_params = {
        'owner_id': -group_id,
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': comment,
    }
    post_url = f'https://api.vk.com/method/wall.post?access_token={access_token}&v=5.131'
    post_response = requests.post(post_url, params=post_params)
    post_response.raise_for_status()


def main():
    load_dotenv()
    access_token = os.getenv('vk_access_token')
    group_id = int(os.getenv('vk_group_id'))
    comic_num = randint(0, 2566)
    url = f'https://xkcd.com/{comic_num}/info.0.json'
    download_comic(url)
    comment = get_comic_comment(url)
    vk_post_images(access_token, group_id, comment)
    os.remove('comic.png')


if __name__ == '__main__':
    main()
