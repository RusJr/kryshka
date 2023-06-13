import json
import re
from time import sleep
from typing import Tuple

from telegram import Bot


class BotTasker:
    RE_TASK = re.compile(r'^(Д|д)елай\W*(?P<url>https?://(\S+\.)?krisha\.kz\S+)')
    NO_TASK_WAITING_PERIOD = 5  # seconds

    def __init__(self, bot: Bot, task_file: str) -> None:
        self._bot = bot
        self._task_file = task_file
        self._url = None
        self._chat_id = None

        self._load_from_file()

    def get_url_and_chat_id(self) -> Tuple:
        self._get_task_from_telegram()
        waiting_message_printed = False

        while not self._url:
            if not waiting_message_printed:
                print('Waiting for a task. Send a message to the bot like '
                      '"Делай https://krisha.kz/prodazha/kvartiry/"')
                waiting_message_printed = True
            sleep(self.NO_TASK_WAITING_PERIOD)
            self._get_task_from_telegram()

        return self._url, self._chat_id

    def _load_from_file(self) -> None:
        try:
            with open(self._task_file) as f:
                file_data = json.loads(f.read())
                self._url = file_data['url']
                self._chat_id = file_data['chat_id']
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self._save_to_file()

    def _save_to_file(self) -> None:
        with open(self._task_file, 'w') as f:
            f.write(json.dumps({'url': self._url, 'chat_id': self._chat_id}))

    def _get_task_from_telegram(self) -> bool:
        for update in self._bot.get_updates()[::-1]:
            text = update.message.text if update.message and update.message.text else None
            if text:
                re_match = self.RE_TASK.match(text)
                if re_match:
                    url = re_match.group('url')
                    chat_id = update.message.chat_id
                    if url and self._url != url and self._chat_id != chat_id:
                        print('Got new task %s' % url)
                        self._url = url
                        self._chat_id = chat_id
                        self._save_to_file()
                        update.message.reply_text('Взял в работу %s' % url)
                    return True
        return False


if __name__ == '__main__':
    from src import conf

    tasker = BotTasker(Bot(conf.BOT_TOKEN), conf.TASK_FILE)
    print(tasker.get_url_and_chat_id())
