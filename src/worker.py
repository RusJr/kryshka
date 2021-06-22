import conf

from time import sleep

from krisa_client import Krisa
from storage import Storage
from telegram import Bot


if __name__ == '__main__':
    krisa = Krisa()
    storage = Storage(conf.FILE)
    bot = Bot(conf.BOT_TOKEN)
    print('Exala...')

    while True:
        haty = krisa.get_haty(conf.SEARCH_URL)
        print('Vot stoka hat: ', len(haty))

        for hata in haty:
            if not storage.is_saved(hata):
                print('VOT ONO', hata)
                bot.sendMessage(conf.CHAT_ID, hata)
                storage.add(hata)
                sleep(0.5)

        sleep(conf.PERIOD)
