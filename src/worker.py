from datetime import datetime

import conf

from time import sleep

from krisa_client import Krisa
from bot_tasker import BotTasker
from storage import Storage
from telegram import Bot


if __name__ == '__main__':
    krisa = Krisa()
    storage = Storage(conf.ARCHIVE_FILE)
    bot = Bot(conf.BOT_TOKEN)
    tasker = BotTasker(bot, conf.TASK_FILE)
    print('Exala...')

    while True:
        search_url, chat_id = tasker.get_url_and_chat_id()

        haty = krisa.get_haty(search_url)
        print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'), 'Vot stoka hat: ', len(haty))

        for hata in haty:
            if not storage.is_saved(hata):
                print('VOT ONO', hata)
                bot.sendMessage(chat_id, hata)
                storage.add(hata)
                sleep(0.5)

        sleep(conf.PERIOD)
