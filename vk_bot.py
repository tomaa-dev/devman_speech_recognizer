import os
import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

from dialogflow_utils import detect_intent_texts


load_dotenv()


def send_message(api, user_id, text):
    api.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(1,1000)
    )


def main():
    vk_token = os.getenv('VK_BOT_TOKEN')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    vk_session = vk_api.VkApi(token=vk_token)
    api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
    	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        	session_id = str(event.user_id)
        	text = event.text
        	answer = detect_intent_texts(project_id, session_id, text)
        	send_message(api, event.user_id, answer)


if __name__ == "__main__":
    main()