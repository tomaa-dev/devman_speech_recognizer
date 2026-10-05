import logging
import os
import random
import time

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow_utils import detect_intent_texts
from logging_utils import setup_logging


logger = logging.getLogger(__name__)


def send_message(api, user_id, text):
    api.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(1,1000)
    )


def main():
    load_dotenv()
    vk_token = os.getenv('VK_BOT_TOKEN')
    tg_token = os.getenv('TG_BOT_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')

    setup_logging(tg_token, tg_chat_id)

    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    vk_session = vk_api.VkApi(token=vk_token)
    api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    session_id = str(event.user_id)
                    text = event.text
                    answer = detect_intent_texts(project_id, session_id, text)
                    if answer:
                        send_message(api, event.user_id, answer)
        except Exception:
            logger.error("VK-бот упал", exc_info=True)
            time.sleep(10)


if __name__ == "__main__":
    main()