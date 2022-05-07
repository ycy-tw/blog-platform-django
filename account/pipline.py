from .models import Account


def access_data(backend, user, response, *args, **kwargs):

    # save profile image

    # from blog.settings import BASE_DIR
    # import urllib.request
    # import os

    # profile_img_url = response['picture']
    # username = user.username
    # save_path = os.path.join(BASE_DIR, 'media', 'images', username, 'profile_img.jpg')
    # urllib.request.urlretrieve(profile_img_url, save_path)
    # user.profile_img = f'images/{username}/profile_img.jpg'

    if Account.objects.filter(email=user.email).exists() is False:

        if len(response['name']) == 0:
            user.name = user.email.split('@')[0]
        else:
            user.name = response['name']
        user.save()
