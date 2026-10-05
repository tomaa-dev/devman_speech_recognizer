import logging
import os
from functools import partial

from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialogflow_utils import detect_intent_texts
from logging_utils import setup_logging


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext, project_id):
    session_id = str(update.effective_user.id)
    text = update.message.text
    answer = detect_intent_texts(project_id, session_id, text)
    if answer:
        update.message.reply_text(answer)


def error_handler(update, context: CallbackContext):
    logger.error("Ошибка в TG-боте", exc_info=context.error)


def main():
    load_dotenv()
    tg_token = os.getenv('TG_BOT_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    setup_logging(tg_token, tg_chat_id)
    
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    
    dispatcher.add_error_handler(error_handler)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo, project_id=project_id))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()