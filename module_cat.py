import requests


def get_cat_photo():
    url = "https://api.thecatapi.com/v1/images/search"
    # количество попыток запроса котика у API
    max_retries = 3
    retries = 0
    photo_url = None

    while retries < max_retries and not photo_url:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                photo_url = response.json()[0]['url']
            except Exception as ex:
                retries += 1
        else:
            retries += 1

    if not photo_url:
        print(f"Не удалось, так как {ex.__class__.__name__}: {ex}")
    return photo_url