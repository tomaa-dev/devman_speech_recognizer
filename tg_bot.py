import logging
import os

from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialogflow_utils import detect_intent_texts
from logging_utils import setup_logging

load_dotenv()

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext):
    session_id = str(update.effective_user.id)
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    text = update.message.text
    answer = detect_intent_texts(project_id, session_id, text)
    if answer:
        update.message.reply_text(answer)


def error_handler(update, context: CallbackContext):
    logger.error("Ошибка в TG-боте", exc_info=context.error)


def main(): 
    setup_logging()

    token = os.getenv('TG_BOT_TOKEN')
    updater = Updater(token)
    dispatcher = updater.dispatcher
    
    dispatcher.add_error_handler(error_handler)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    logger.info("Бот запущен")

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()