import logging
import os

import telegram


class MyLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self.bot.send_message(chat_id=self.chat_id, text=log_entry)
        except Exception:
            self.handleError(record)


def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
    )

    tg_token = os.getenv('TG_BOT_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    bot = telegram.Bot(token=tg_token)

    handler = MyLogsHandler(bot, chat_id)
    handler.setLevel(logging.ERROR)
    handler.setFormatter(logging.Formatter('%(message)s'))

    logging.getLogger().addHandler(handler)
    logging.getLogger('telegram').addHandler(handler)

    return handler