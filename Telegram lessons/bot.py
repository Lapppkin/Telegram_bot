# -*- coding: utf-8 -*-
import config
import telebot
from telebot import apihelper

apihelper.proxy = {'https':'socks5://user38375:1skmnu@213.32.84.49:13541'}
# apihelper.proxy = {'https':'SOCKS5://193.111.155.211:16608'}
# apihelper.proxy = {'https':'https://193.111.155.211:6608'}


bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
     bot.infinity_polling()


