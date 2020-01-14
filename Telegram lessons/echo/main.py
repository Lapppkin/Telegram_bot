import datetime
from telegram import Bot
from telegram import Update
from telegram import InlineKeyboardButton # Отвечает за отдельную клавишу
from telegram import InlineKeyboardMarkup # Отвечает за всю клавиатуру вцелом
from telegram import ParseMode
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler # Отвечает за обработку нажатия на клавиши



from echo.config import TG_TOKEN
from echo.config import TG_API_URL

# `callback_data` -- это то, что будет присылать TG при нажатии на каждую кнопку.
# Поэтому каждый идентификатор должен быть уникальным
CALLBACK_BUTTON_LEFT = 'callback_button_left'
CALLBACK_BUTTON_RIGHT = 'callback_button_right'
CALLBACK_BUTTON_BACK = 'callback_button_back'

TITLES = {
    CALLBACK_BUTTON_LEFT: 'Напоминания',
    CALLBACK_BUTTON_RIGHT: 'В разработке',
    CALLBACK_BUTTON_BACK: 'Назад',
}


def get_base_inline_keyboard():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где ее прикрепили
    """
    # Каждый список внутри "Keyboard" -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_LEFT], callback_data=CALLBACK_BUTTON_LEFT),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_RIGHT], callback_data=CALLBACK_BUTTON_RIGHT),

        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_callback_handler(bot: Bot, update: Update, chat_data=None, **kwargs):
    """ Обработчик ВСЕХ кнопок со ВСЕХ клавиатур
    """
    query = update.callback_query
    data = query.data
    now = datetime.datetime.now()

    # Обратите внимание: используется 'effective_message'
    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text

    if data == CALLBACK_BUTTON_LEFT:
        # "Удалим" клавиатуру у прошлого сообщения
        # (на самом деле отредактируем его так, что текст останется тот же, а клавиатура пропадет)
        query.edit_message_text(
            text=current_text,
            parse_mode=ParseMode.MARKDOWN,
        )
        # Отправим новое сообщение при нажатии на кнопку
        bot.send_message(
            chat_id=chat_id,
            text=f'О чем Вам напомнить?',
        )
    elif data == CALLBACK_BUTTON_RIGHT:
        pass
    else:
        pass



def do_start(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    user_name = update.message.from_user.first_name
    bot.send_message(
        chat_id=chat_id,
        text=f'Привет, {user_name}! 🖖',
    )


def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    user_name = update.message.from_user.first_name
    user_text = update.message.text
    text = f"Ваш ID = {chat_id}\n\n{user_text}"
    if str.lower(update.message.text) == str.lower('Привет'):
        bot.send_message(
            chat_id=chat_id,
            text=f'Приветствую =)\n\nВыберите функцию из списка:',
            reply_markup=get_base_inline_keyboard(),
            )
        # Добавляем кнопки
        # bot.send_message(message.chat.id, 'О чем Вам напомнить?')
        # bot.send_message(message.chat.id, 'Напишите что хотите запомнить')

    elif str.lower(update.message.text) == str.lower('Как дела?'):
        bot.send_message(
            chat_id=chat_id,
            text=f'Спасибо, что спросили, у меня Все хорошо!')

    elif update.message.text == 'help':
        bot.send_message(
            chat_id=chat_id,
            text=f'Напиши - "Привет!"')
    else:
        bot.send_message(
            chat_id=chat_id,
            text=f'{user_name}, я тебя не понимаю.\nВведи команду "help"')



def remind_text(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    user_text = update.message.text
    bot.send_message(
        chat_id=chat_id,
        text=f'Через сколько Вам напомнить: \n{user_text}',
        reply_markup=get_base_inline_keyboard(),
    )



    # bot.send_message(
    #     chat_id=chat_id,
    #     text='О чем Вам напомнить?',
    # )



def main():
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler('start', do_start)
    message_handler = MessageHandler(Filters.text, do_echo)
    buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler, pass_chat_data=True)


    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(buttons_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
