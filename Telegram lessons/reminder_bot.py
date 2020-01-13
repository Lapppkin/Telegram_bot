import telebot
from telebot import apihelper
from telebot import types
import time
import _sqlite3

# db = _sqlite3.connect('reminder_db.sqlite') # создаем переменную и подключаем базу данных

apihelper.proxy = {'https': 'socks5://user38375:1skmnu@213.32.84.49:13541'} # Подключаем прокси для работы с Telegram
# apihelper.proxy = {'https':'https://user38375:1skmnu@213.32.84.49:3541'}

bot = telebot.TeleBot('1054775144:AAGR0Pu07k2Ql7VdhleiKL1bl79J6keAEfA') # Подключаем токен нашего бота

"""
Бот-запоминатель-проверятель, который помогает учить иностранные слова (или другие штуки).

Суть: отправляешь боту слово (фразу), которое хочешь запомнить. Потом перевод (или значение). Бот запоминает комбинацию и будет проверять тебя в будущем. Согласно графику бот отправит тебе напоминание (покажет и слово, и перевод), а затем (согласно настройкам) проверку (покажет слово и спросит перевод). После N удачных ответов подряд (настраивается в настройках), бот перестанет напоминать это слово.

Пример:
U: dog
B: Какой перевод? 
U: собака
B: Окей. Напомню позже.
...
B: dog — собака
...
B: dog — ...
U: кот
B: Неверно.
U: собака
B: Верно. Проверим позже.
...
B: собака — ...
U: god
B: неверно
U: dog
B: Верно. Проверю еще разок позже.
...

Расписание проверок настраивается как угодно. Каждый может настроить под свой стиль запоминания.
"""

# cursor = db.cursor()
# cursor.execute('''
# CREATE TABLE reminders (
#     id INTEGER PRIMARY KEY,
#     user_id INTEGER NOT NULL,
#     reminde_text TEXT NOT NULL UNIQUE
# )
# ''')  # создаем запрос - создаем таблицу


# def Write_to_Base(user_id, rem_text):
#     user_id = str(user_id)
#     rem_text = str(rem_text)
#     cursor.execute("INSERT INTO reminders (tele_id, key) VALUES('"+user_id+","+rem_text+"')")
#     conn.commit()

# bot.message_handler(commands=['user_id_catcher'])
# def regist_message(message):
#     user_id = message.from_user.id
#     print(user_id)
#     bot.send_message(message.chat.id, f'Держи {user_id}')

# Обрабатывает все текстовые сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! 🖐')


# Теперь научим бота реагировать на слово «Привет»
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if str.lower(message.text) == str.lower('Привет'):
        bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name} =)')

        # Добавляем кнопки
        # Добавляем код с кнопками в раздел, который реагирует на «Привет»:
        keyboard = types.InlineKeyboardMarkup()

        # По очереди готовим текст и обработчик для каждого 'элемента'(кнопки)
        key_one = types.InlineKeyboardButton(text='Напоминалка', callback_data='menu_one')


        # И добавляем кнопку на экран
        keyboard.add(key_one)


        # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.chat.id, text='Выбери программу', reply_markup=keyboard)

    elif message.text == '/help':
        bot.send_message(message.chat.id, f'Напиши - "Привет!"')

    else:
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, я тебя не понимаю.\nВведи команду "/help"')


@bot.message_handler(content_types=['text'])
def remind_text(message):

    user_text = message.text

    # bot.register_next_step_handler(user_text, callback_worker)

    # bot.send_message(message.chat.id, f'{message.from_user.first_name}, через сколько Вам напомнить:\n{user_text}')

    keyboard_rem = types.InlineKeyboardMarkup()

    key_zero_rem = types.InlineKeyboardButton(text='1 минута', callback_data='01_min')
    key_one_rem = types.InlineKeyboardButton(text='30 минут', callback_data='30_min')
    key_two_rem = types.InlineKeyboardButton(text='60 минут', callback_data='60_min')
    key_tree_rem = types.InlineKeyboardButton(text='90 минут', callback_data='90_min')
    key_four_rem = types.InlineKeyboardButton(text='xx минут', callback_data='xx_min')

    # И добавляем кнопку на экран
    keyboard_rem.add(key_zero_rem)
    keyboard_rem.add(key_one_rem)
    keyboard_rem.add(key_two_rem)
    keyboard_rem.add(key_tree_rem)
    keyboard_rem.add(key_four_rem)

    # Показываем все кнопки сразу и пишем сообщение о выборе
    bot.send_message(message.chat.id, text=f'{message.from_user.first_name}, '
                                           f'через сколько Вам напомнить: \n{user_text}', reply_markup=keyboard_rem)

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    if call.data == 'menu_one':
        sent = bot.send_message(call.message.chat.id, 'О чем Вам напомнить?')
        bot.register_next_step_handler(sent, remind_text)

        # Ждём ответа пользователя и результат помещаем в строковую переменную text
    # elif call.data == 'menu_two':
    elif call.data == '01_min':
        bot.send_message(call.message.chat.id, 'Будет сделано через 1 минуту =)')
        local_time = float(0.1)
        local_time = local_time * 60
        time.sleep(local_time)
        msg1 = f'НАПОМИНАЮ: ТУТ БУДЕТ ТЕКСТ ВАШЕГО НАПОМИНАНИЯ' # Нужно решить как можно вывести повторно текст напоминания.
        bot.send_message(call.message.chat.id, msg1)

    elif call.data == '30_min':
        bot.send_message(call.message.chat.id, 'Будет сделано через 30 минут =)')
        local_time = float(30)
        local_time = local_time * 60
        time.sleep(local_time)
        msg1 = f'НАПОМИНАЮ: ТУТ БУДЕТ ТЕКСТ ВАШЕГО НАПОМИНАНИЯ' # Нужно решить как можно вывести повторно текст напоминания.
        bot.send_message(call.message.chat.id, msg1)

    elif call.data == '60_min':
        bot.send_message(call.message.chat.id, 'Будет сделано через 60 минут =)')
        local_time = float(60)
        local_time = local_time * 60
        time.sleep(local_time)
        msg1 = f'НАПОМИНАЮ: ТУТ БУДЕТ ТЕКСТ ВАШЕГО НАПОМИНАНИЯ'  # Нужно решить как можно вывести повторно текст напоминания.
        bot.send_message(call.message.chat.id, msg1)

    elif call.data == '90_min':
        bot.send_message(call.message.chat.id, 'Будет сделано через 90 минут =)')
        local_time = float(90)
        local_time = local_time * 60
        time.sleep(local_time)
        msg1 = f'НАПОМИНАЮ: ТУТ БУДЕТ ТЕКСТ ВАШЕГО НАПОМИНАНИЯ'  # Нужно решить как можно вывести повторно текст напоминания.
        bot.send_message(call.message.chat.id, msg1)

    elif call.data == 'xx_min':
        bot.send_message(call.message.chat.id, 'Будет сделано через xx минут =)')
        local_time = float(0)
        local_time = local_time * 60
        time.sleep(local_time)
        msg1 = f'НАПОМИНАЮ: ТУТ БУДЕТ ТЕКСТ ВАШЕГО НАПОМИНАНИЯ'  # Нужно решить как можно вывести повторно текст напоминания.
        bot.send_message(call.message.chat.id, msg1)

    else:
        pass

# Обработчик нажатий на кнопки 2
# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker_rem(call2):
#     if call2.data == '30_min':
#         bot.send_message(call2.chat.id, 'Будет сделано =)')
        # local_time = local_time * 30
        # time.sleep(local_time)
        # msg1 = user_text
        # bot.send_message(call.data.message.chat.id, msg1)
#
#
#
#         # sent = bot.send_message(call.message.chat.id, 'О чем вам напомнить?')
#         # bot.register_next_step_handler(sent, remind_text)
#         # Ждём ответа пользователя и результат помещаем в строковую переменную text
#
#     elif call.data == '60_min':
#         pass # local_time = local_time * 60
#     elif call.data == '90_min':
#         pass # local_time = local_time * 90
#     else:
#         pass


# @bot.message_handler(content_types=['text'])
# def get_text_remind_messages(message):
#     remind_text = message.text
#     print(remind_text)
#     bot.register_next_step_handler(remind_text)
#
#     bot.send_message(message.chat.id, f'Через сколько напомнить - {remind_text}')


bot.polling(none_stop=True, interval=0)

