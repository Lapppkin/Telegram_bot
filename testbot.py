import telebot
from telebot import apihelper
from telebot import types

apihelper.proxy = {'https':'socks5://user38375:1skmnu@213.32.84.49:13541'}
# apihelper.proxy = {'https':'https://user38375:1skmnu@213.32.84.49:3541'}

bot = telebot.TeleBot('1054775144:AAGR0Pu07k2Ql7VdhleiKL1bl79J6keAEfA')


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
		key_one = types.InlineKeyboardButton(text='One', callback_data='menu_one')
		key_two = types.InlineKeyboardButton(text='Two', callback_data='menu_two')
		key_tree = types.InlineKeyboardButton(text='Tree', callback_data='menu_tree')

		# И добавляем кнопку на экран
		keyboard.add(key_one)
		keyboard.add(key_two)

		# Показываем все кнопки сразу и пишем сообщение о выборе
		bot.send_message(message.chat.id, text='Выбери свой пункт меню', reply_markup=keyboard)
	elif message.text == '/help':
		bot.send_message(message.chat.id, f'Напиши - "Привет!"')
	else:
		bot.send_message(message.chat.id, f'{message.from_user.first_name}, я тебя не понимаю.\nВведи команду "/help"')


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    # Если нажали на одну из 2 кнопок — выводим данные/текст

    if call.data == "menu_one":

        # Формируем гороскоп

        msg = random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(second_add) + ' ' + random.choice(third)

        # Отправляем  текст в Телеграм

        bot.send_message(call.message.chat.id, msg)







# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if str.lower(message.text) == str.lower('Привет' or 'Здравствуйте' or 'Здравствуй'):
#         bot.send_message(message.from_user.id, 'Приветствую, чем я могу тебе помочь?')
#     elif message.text == '/help':
#         bot.send_message(message.from_user.id, 'Напиши привет или спроси меня что я умею')
#     elif str.lower(message.text) == str.lower('Кто ты') or str.lower('Кто ты?'):
#         bot.send_message(message.from_user.id, 'Я тестовый чатбот для учебного примера.')
#     elif str.lower(message.text) == str.lower('Как тебя зовут?' or 'Как тебя зовут' or 'Как тебя звать'):
#         bot.send_message(message.from_user.id, 'Меня зовут Бот Артур =).')
#     elif str.lower(message.text) == str.lower('Что ты умеешь?'):
#         bot.send_message(message.from_user.id, 'Я умею отвечать на несколько простых вопросов' +
#                          '- кто я, как меня зовут и что я умею делать.')
#     else:
#         bot.send_message(message.from_user.id, 'Я тебя не понимаю. Напиши /help.')

bot.polling(none_stop=True, interval=0)

# bot.send_message(chat_id, text)
# markup = types.ReplyKeyboardMarkup(row_width=2)
# itembtn1 = types.KeyboardButton('a')
# itembtn2 = types.KeyboardButton('v')
# itembtn3 = types.KeyboardButton('d')
# markup.add(itembtn1, itembtn2, itembtn3)
# bot.send_message(chat_id, "Choose one letter:", reply_markup=markup)







