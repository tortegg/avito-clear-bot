import logging
from aiogram import Bot, Dispatcher, executor, types
import requests
from bs4 import BeautifulSoup
import re
from PIL import Image
import os
import shutil
import asyncio
import time


# Объект бота
bot = Bot(token="2111875221:AAFCD5tJm8BhSfPhELflFg7rsk4nBv-X6eI")
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Хэндлер на команду /start
@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    await message.reply("привет лентяй, не хочешь фоткать обект? Скинь ссылку на авито ;)")

@dp.message_handler()
async def avito_link_message(message: types.Message):
    try:
        await message.answer('Подождите')
        name1 = 1
        url = message.text
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        folder_name1 = soup.find('span', {'data-marker': 'item-view/item-id'}).string[2:]
        data = soup.find('div', {'class': "gallery-img-frame js-gallery-img-frame"})['data-url']
        link = data[:24] + "/1280x960/"
        for tag in soup.find_all('meta', {'property': "og:image"}):  # ['content']
            keys = tag['content']
            image_url = link + keys[36:] + '.jpg'
            img_data = requests.get(image_url).content
            print(str(name1) + 'photo load')
            with open(str(name1) + '.jpg', 'wb') as handler:
                handler.write(img_data)
                name1 += 1

        time.sleep(3)

        namepapka = str(folder_name1)
        papka = 'Photos/' + namepapka
        if not os.path.exists(papka):
            os.makedirs(papka)
        name = 17
        try:  # тут обрезаем логотип и ловим экспет на выход из цикла
            for pic in papka:
                name1 -= 1
                img = Image.open(str(name1) + '.jpg')
                #обрезает 17 файлов и выходит из цикла почему то
                w, h = img.size
                img.crop((0, 0, w, h - 49)).save(str(papka) + '/' + str(name1) + '.jpg')
                os.remove(str(name1) + '.jpg')
                print(str(name1) + ' cropped')
        except FileNotFoundError:
            print('готово')

        time.sleep(3)

        shutil.make_archive(namepapka, 'zip', papka)  # создает ахив с фотками в корневом каталоге(переделать чтобы сохранял в ту же папку)
        shutil.rmtree(papka, ignore_errors=True)
        #await asyncio.sleep(5.0)
        await message.answer_document(open(namepapka + '.zip', 'rb'))
        #await asyncio.sleep(5.0)
        os.remove(namepapka + '.zip')
    except requests.exceptions.MissingSchema as e:
        await message.answer('пришли ссылку в виде "https://avito.ru/***"')



if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)