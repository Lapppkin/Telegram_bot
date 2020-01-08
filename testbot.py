import telebot
from telebot import apihelper
from telebot import types

apihelper.proxy = {'https':'socks5://user38375:1skmnu@213.32.84.49:13541'}

bot = telebot.TeleBot('1054775144:AAGR0Pu07k2Ql7VdhleiKL1bl79J6keAEfA')


# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
# 	bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Привет' or 'привет':
        bot.send_message(message.from_user.id, 'Привет, чем я могу тебе помочь?')
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Напиши привет')
    elif message.text == "Кто ты?":
        bot.send_message(message.from_user.id, 'Я тестовый чатбот для учебного примера.')
    elif message.text == 'Как тебя зовут?':
        bot.send_message(message.from_user.id, 'Меня зовут MyFirstTestBot.')
    elif message.text == 'Что ты умеешь?':
        bot.send_message(message.from_user.id, 'Я умею отвечать на несколько простых вопросов' +
                         '- кто я, как меня зовут и что я умею делать.')
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю. Напиши /help.')

bot.polling(none_stop=True, interval=0)

# bot.send_message(chat_id, text)
# markup = types.ReplyKeyboardMarkup(row_width=2)
# itembtn1 = types.KeyboardButton('a')
# itembtn2 = types.KeyboardButton('v')
# itembtn3 = types.KeyboardButton('d')
# markup.add(itembtn1, itembtn2, itembtn3)
# bot.send_message(chat_id, "Choose one letter:", reply_markup=markup)







