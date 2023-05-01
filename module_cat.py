import logging
import requests

async def get_cat_photo():
    url = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(url)
    photo_url = response.json()[0]['url']

    return photo_url
    # await bot.send_photo(chat_id=message.chat.id, photo=InputFile.from_url(photo_url))
