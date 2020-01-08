import telebot
bot = telebot.TeleBot('1054775144:AAGR0Pu07k2Ql7VdhleiKL1bl79J6keAEfA')


@bot.add_message_handler(content_types=['text', 'document', 'audio'])
def get_text_messages(message):

