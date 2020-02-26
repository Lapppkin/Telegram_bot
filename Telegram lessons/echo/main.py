import datetime
from logging import getLogger
from telegram import Bot
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
# from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler # Отвечает за обработку нажатия на клавиши
from telegram.utils.request import Request




from settings.production import TG_TOKEN
from settings.production import TG_API_URL
from echo.config import load_config


config = load_config()

logger = getLogger(__name__)



def do_start(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    user_name = update.message.from_user.first_name
    bot.send_message(
        chat_id=chat_id,
        text=f'Привет, {user_name}! 🖖',
    )


def do_help(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    bot.send_message(
        chat_id=chat_id,
        text=f'Напиши - "Привет" 🖖',
    )


def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    user_name = update.message.from_user.first_name
    user_text = update.message.text
    # text = f"Ваш ID = {chat_id}\n\n{user_text}"
    # bot.send_message(
    #     chat_id=chat_id,
    #     text=text,
    # )

    if str.lower(update.message.text) == str.lower('Привет'):
        bot.send_message(
            chat_id=chat_id,
            text=f'Приветствую =)\n\nНапишите, о чем Вам напомнить?',
            )
    else:
        bot.send_message(
            chat_id=chat_id,
            text=f'{user_name}, я тебя не понимаю.\nВведи команду "/help"')
    return 'reminder'


# def do_reminder(bot: Bot, update: Update):
#     chat_id = update.message.chat_id
#     text = update.message.text
#     # Получить текст напоминания
#
#     if user_data:
#         bot.send_message(
#             chat_id=chat_id,
#             text=f'Ваш текст - {user_data}! 🖖',
#         )




def main():

    logger.info("Запускаем бота...")

    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )

    bot = Bot(
        token=TG_TOKEN,
        request=req,
        base_url=TG_API_URL,
    )
    updater = Updater(
        bot=bot,
        # request_kwargs={
        #     'proxy_url': 'socks5://213.32.84.49:13541/'
        # },
        # use_context=True,

    )

    # Проверить что бот корректно подключился к Telegram API
    info = bot.get_me()
    logger.info(f'Bot info: {info}')


    start_handler = CommandHandler('start', do_start)
    help_handler = CommandHandler('help', do_help)
    message_handler = MessageHandler(Filters.text, do_echo)
    # reminder_handler = MessageHandler(Filters.text, do_reminder)
    # buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler, pass_chat_data=True)


    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(message_handler)
    # updater.dispatcher.add_handler(reminder_handler)
    # updater.dispatcher.add_handler(buttons_handler)

    updater.start_polling()
    updater.idle()

    logger.info("Закончили...")



if __name__ == '__main__':
    main()
