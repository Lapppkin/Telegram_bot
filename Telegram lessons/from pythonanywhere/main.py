from telegram import Bot
from telegram import Update
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram import ParseMode
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.utils.request import Request


import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


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

button_1 = 'Напоминания'
BUTTON1_HELP = "Помощь"


def log_error(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'Ошибка: {e}')
            raise e

    return inner

def get_base_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON1_HELP),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def get_base_inline_keyboard():
    """ Получить клавиатуру для сообщения
        Эта клавиатура будет видна под каждым сообщением, где её прикрепили
    """
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_LEFT], callback_data=CALLBACK_BUTTON_LEFT),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_RIGHT], callback_data=CALLBACK_BUTTON_RIGHT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_BACK], callback_data=CALLBACK_BUTTON_BACK),
        ],

    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_callback_handler(update: Update, context: CallbackContext):
    """ Обработчик ВСЕХ кнопок со ВСЕХ клавиатур
    """
    query = update.callback_query
    data = query.data

    # Обратите внимание: используется `effective_message`
    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text

    if data == CALLBACK_BUTTON_LEFT:
        # "Удалим" клавиатуру у прошлого сообщения
        # (на самом деле отредактируем его так, что текст останется тот же, а клавиатура пропадёт)
        query.edit_message_text(
            text='Напишите о чем Вам напомнить?',
            parse_mode=ParseMode.MARKDOWN,
        )

    # Отправим новое сообщение при нажатии на кнопку
    #     context.bot.send_message(
    #         chat_id=chat_id,
    #         text=f'Новое сообщение\n\n{update.callback_query}',
    #         reply_markup=get_base_inline_keyboard(),
    #    )
    # elif data == CALLBACK_BUTTON2_RIGHT:
    #     # Отредактируем текст сообщения, но оставим клавиатуру
    #     query.edit_message_text(
    #         text="Успешно отредактировано в {}".format(now),
    #         reply_markup=get_base_inline_keyboard(),
    #     )
    # elif data == CALLBACK_BUTTON3_MORE:
    #     # Показать следующий экран клавиатуры
    #     # (оставить тот же текст, но указать другой массив кнопок)
    #     query.edit_message_text(
    #         text=current_text,
    #         reply_markup=get_keyboard2(),
    #     )
    # elif data == CALLBACK_BUTTON4_BACK:
    #     # Показать предыдущий экран клавиатуры
    #     # (оставить тот же текст, но указать другой массив кнопок)
    #     query.edit_message_text(
    #         text=current_text,
    #         reply_markup=get_base_inline_keyboard(),
    #     )
    # elif data == CALLBACK_BUTTON5_TIME:
    #     # Покажем новый текст и оставим ту же клавиатуру
    #     text = "*Точное время*\n\n{}".format(now)
    #     query.edit_message_text(
    #         text=text,
    #         parse_mode=ParseMode.MARKDOWN,
    #         reply_markup=get_keyboard2(),
    #     )
    # elif data in (CALLBACK_BUTTON6_PRICE, CALLBACK_BUTTON7_PRICE, CALLBACK_BUTTON8_PRICE):
    #     pair = {
    #         CALLBACK_BUTTON6_PRICE: "USD-BTC",
    #         CALLBACK_BUTTON7_PRICE: "USD-LTC",
    #         CALLBACK_BUTTON8_PRICE: "USD-ETH",
    #     }[data]

    #     try:
    #         current_price = client.get_last_price(pair=pair)
    #         text = "*Курс валюты:*\n\n*{}* = {}$".format(pair, current_price)
    #     except BittrexError:
    #         text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
    #     query.edit_message_text(
    #         text=text,
    #         parse_mode=ParseMode.MARKDOWN,
    #         reply_markup=get_keyboard2(),
    #     )
    elif data == CALLBACK_BUTTON_BACK:
        # Спрятать клавиатуру
        # Работает только при отправке нового сообщение
        # Можно было бы отредактировать, но тогда нужно точно знать что у сообщения не было кнопок
        context.bot.send_message(
            chat_id=chat_id,
            text="Вернулись к началу\n\nНажмите /start чтобы начать снова",
            reply_markup=ReplyKeyboardRemove(),
        )


def do_start(update: Update, context: CallbackContext):
    user_name = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Привет, {user_name}! 🖖',
        reply_markup=get_base_reply_keyboard()
        )


def do_help(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Напиши - "Привет" 🖖'
        )


def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    if text == BUTTON1_HELP:
        return do_help(update=update, context=context)

    elif text == str('Привет') or str('привет'):
        # user_text = update.message.text
        update.message.reply_text(
            # text=user_text,
            text='Выберите пункт: ',
            reply_markup=get_base_inline_keyboard(),
        )
    elif text == f'напомни {text}':
        # Отправим новое сообщение при нажатии на кнопку
        context.bot.send_message(
            chat_id=chat_id,
            text=f'Новое сообщение\n\n{update.message.text}',
            )

    # elif text == BUTTON2_TIME:
    #     pass
    else:
        return do_help(update=update, context=context)
        # # user_text = update.message.text
        # update.message.reply_text(
        #     # text=user_text,
        #     text='Выберите пункт: ',
        #     reply_markup=get_base_inline_keyboard(),
        # )

    # context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text=f'Вы ввели - {user_text}'
    #     )
    # return user_text


# def do_button_1_handler(update: Update, context: CallbackContext):
#     update.message.reply_text(
#         text='Напоминания!',
#         reply_markup=ReplyKeyboardRemove(),
#     )


# def do_message_handler(update: Update, context: CallbackContext):
#     text = update.message.text
#     if text == button_1:
#         return button_1_handler(update=update, context=context)

#     reply_markup = ReplyKeyboardMarkup(
#         keyboard=[
#             [
#                 KeyboardButton(text=button_1),
#             ],
#         ],
#         resize_keyboard=True,
#     )

#     update.message.reply_text(
#         text='Привет, нажми кнопку ниже!',
#         reply_markup=reply_markup,
#     )


# @log_error
# def message_handler(update: Update, context: CallbackContext):
#     text = update.message.text
#     if text == button_help:
#         return button_help_handler(update=update, context=context)

#     reply_markup = ReplyKeyboardMarkup(
#         keyboard=[
#             [
#                 KeyboardButton(text=button_help),
#             ],
#         ],
#         resize_keyboard=True,
#     )

#     update.message.reply_text(
#         text='Привет, нажми кнопку ниже!',
#         reply_markup=reply_markup,
#     )


def main():
    print('Start')

    req = Request(
        connect_timeout=0.5,
    )
    bot = Bot(
        request=req,
        token='1054775144:AAGR0Pu07k2Ql7VdhleiKL1bl79J6keAEfA',
        # base_url='https://telegg.ru/orig/bot',
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )
    print(updater.bot.get_me())

    start_handler = CommandHandler('start', do_start)
    help_handler = CommandHandler('help', do_help)
    message_handler = MessageHandler(Filters.text, do_echo)
    # button_message_handler = MessageHandler(Filters.text, do_message_handler)
    # button_1_handler = MessageHandler(Filters.text, do_button_1_handler)
    buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(message_handler)
    # updater.dispatcher.add_handler(button_message_handler)
    # updater.dispatcher.add_handler(button_1_handler)
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))
    updater.dispatcher.add_handler(buttons_handler)

    updater.start_polling()
    updater.idle()

    print('Finish')


if __name__ == '__main__':
    main()