# подключение библиотек и файлов
import telebot
import config
from mintersdk import minterapi
import time
import requests
import json
import base64
import sqlite3
import re
import threading
import datetime
import pytz

database = config.database  # база данных

bot_token = config.bot_token  # токен телеграм бота
channgel_name = config.channel  # имя канала для постинга

minter_api = config.minter_api  # api minter
minter_api_headers = config.minter_api_headers  # keys for api minter

address_for_listening = config.address_for_listening  # адрес для транзакций

bot = telebot.TeleBot(bot_token)  # создание бота

hyperlink_format = '<a href="{0}">{1}</a>'  # шаблон для гиперссылки

minterscan_icon_link = config.minterscan_icon_link  # ссылка для определения иконки кошелька

minterscan_address_link = config.minterscan_address_link  # ссылка на адрес

explorer_transaction_link = config.explorer_transaction_link  # ссылка на транзакцию

message_template = '{emoji} {from_address}\n\n{payload}\n\n{coin}'  # шаблон сообщения


# SQL функции

def insert_into_transactions(hash, from_address, coin, value, payload, status):
    """
    Создает новую запись в таблице transactions
    :param hash: str
    :param from_address: str
    :param coin: str
    :param value: float
    :param payload: str
    :param status: str
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    ex = "insert into transactions values ('{}', '{}', '{}',{}, '{}', '{}')".format(hash, from_address, coin, value,
                                                                                    payload, status)
    cursor.execute(ex)
    conn.commit()
    conn.close()


def insert_into_pinned(message_id, time_unpin):
    """
    Создает новую запись в таблице pinned
    :param message_id: int
    :param time_unpin: str
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    ex = "insert into pinned values ({}, '{}')".format(message_id, time_unpin)
    cursor.execute(ex)
    conn.commit()
    conn.close()


def get_unpin(now_time):
    """
    Запрашивает запись со временем now_time из таблицы pinned
    :param now_time:
    :return: int or bool
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    ex = "select message_id from pinned where time_unpin = '{}'".format(now_time)
    cursor.execute(ex)
    res = cursor.fetchall()
    conn.commit()
    conn.close()
    return res[0][0] if len(res) else False


def delete_from_pinned():
    """
    Удаляет все записи из таблицы pinned
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    ex = "delete from pinned"
    cursor.execute(ex)
    conn.commit()
    conn.close()


# внутренние функции
def check_for_link(text):
    """
    Проверяет текст на ссылки
    :param text: str
    :return: bool
    """
    regex = r"(?P<domain>\w+\.\w{2,3})"
    r = re.search(regex, text)
    if r or '@' in text:
        return True
    return False


def check_for_delegator(address):
    """
    Проверяет является ли пользователь делегатором
    :param address: str
    :return: bool
    """
    data = json.loads(requests.get(config.link_explorer_delegations.format(address)).text)['data']
    for i in data:
        if i['coin'] == config.coin_for_limit and float(i['value']) >= config.limit_delegator_coin:
            return True
    return False


def get_icon(address):
    """
    Определяет иконку кошелька. При невозможности проверить автоматически, возвращает неопределенную иконку.
    :param address: str
    :return: str
    """
    try:
        icon = requests.get(minterscan_icon_link.format(address)).text
        return icon
    except:
        return '🤔'


def now_time():
    """
    Приводит текущее время без секунд (МСК) к строчному формату (YYYY-MM-DDTHH:MM+03:00)
    :return: str
    """
    tzlocal = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(tzlocal)
    s = ''
    s += str(now.year) + '-'
    if len(str(now.month)) > 1:
        s += str(now.month)
    else:
        s += '0' + str(now.month)
    s += '-'
    if len(str(now.day)) > 1:
        s += str(now.day)
    else:
        s += '0' + str(now.day)
    s += 'T'
    if len(str(now.hour)) > 1:
        s += str(now.hour)
    else:
        s += '0' + str(now.hour)
    s += ':'
    if len(str(now.minute)) > 1:
        s += str(now.minute)
    else:
        s += '0' + str(now.minute)
    return s


def time_delta(period):
    """
    Высчитывает определенный промежуток во времени. Возвращает время без секунд (МСК) в строчном формате (YYYY-MM-DDTHH:MM+03:00)
    :param period: str (hour or day)
    :return: str
    """
    tzlocal = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(tzlocal)

    if period == 'hour':
        delta_time = now + datetime.timedelta(hours=1)
    elif period == 'day':
        delta_time = now + datetime.timedelta(days=1)
    s = ''
    s += str(delta_time.year) + '-'
    if len(str(delta_time.month)) > 1:
        s += str(delta_time.month)
    else:
        s += '0' + str(delta_time.month)
    s += '-'
    if len(str(delta_time.day)) > 1:
        s += str(delta_time.day)
    else:
        s += '0' + str(delta_time.day)
    s += 'T'
    if len(str(delta_time.hour)) > 1:
        s += str(delta_time.hour)
    else:
        s += '0' + str(delta_time.hour)
    s += ':'
    if len(str(delta_time.minute)) > 1:
        s += str(delta_time.minute)
    else:
        s += '0' + str(delta_time.minute)
    return s


def pin_message(period, message_info):
    """
    Закрепляет сообщение, предварительно удалив предыдущее закрепленное.
    :param period: str
    :param message_info: message
    """
    delete_from_pinned()
    bot.pin_chat_message(channgel_name, message_info.message_id)
    insert_into_pinned(message_info.message_id, time_delta(period))


def unpinner():
    """
    Функция для отдельного потока, открепляющего сообщения, для которых закончилось время закрепления.
    """
    while True:
        if get_unpin(now_time()):
            bot.unpin_chat_message(channgel_name)
            delete_from_pinned()
        time.sleep(60)


unpinner_thread = threading.Thread(target=unpinner,
                                   name='unpinner_thread')  # определение отдельного потока для открепления сообщений
unpinner_thread.start()  # запуск потока

'''
# модификация для корректной работы с заголовками для funfasy.dev
class MinterAPIService(minterapi.MinterAPI):
    request_headers = minter_api_headers

    def _request(self, command, request_type='get', **kwargs):
        kwargs['headers'] = self.request_headers
        aa = super()._request(command, request_type=request_type, **kwargs)
        if 'result' in aa.keys():
            return aa['result']
        else:
            return aa
'''

MinterNode = minterapi.MinterAPI(api_url=minter_api, headers=minter_api_headers)  # объект для работы с minter api

# предварительный запрос последних транзакций на кошелек
# значение page предельно большое для обозначения того, что нужна последняя страница
txns = MinterNode.get_transactions(query="tags.tx.to='{}'".format(address_for_listening), page=100000000000)['result']
while True:
    # повторный запрос последних транзакций
    txns2 = MinterNode.get_transactions(query="tags.tx.to='{}'".format(address_for_listening), page=100000000000)['result']
    print('ВСЕ ОК, РАБОТАЮ - ', txns2)
    # для каждой транзакции в повторном запросе, если она отсутствует в предыдущем
    for i in txns2:
        if i not in txns:
            icon = get_icon(i['from'])  # определение иконки
            from_address = i['from']  # определение адреса отправителя
            from_address_short = from_address[:6] + '...' + from_address[
                                                            -4:]  # приведение адреса отправителя к формату MxAAAA...AAAA
            payload = base64.b64decode(i['payload']).decode(
                'utf-8')  # получение сообщения из payload и приведение его к utf-8
            coin = i['data']['coin']  # определение монеты
            value = float("{0:.3f}".format(int(i['data']['value']) / 10 ** 18))  # определение суммы
            value_coin = str(value) + ' ' + coin  # совмещение суммы и монеты
            value_coin = hyperlink_format.format(explorer_transaction_link.format(i['hash'].lower()),
                                                 value_coin)  # создание гиперссылки на транзакцию
            from_address = hyperlink_format.format(minterscan_address_link.format(from_address),
                                                   from_address_short)  # создание гиперссылки на адрес отправителя
            message_text = message_template.format(emoji=icon, from_address=from_address, payload=payload,
                                                   coin=value_coin)  # создание текста сообщения
            # проверка на соответствие минимальным требованиям (сумма, монета, не пустое сообщение)
            if value >= config.price_for_ordinary_message and coin == config.coin_for_limit and payload:
                # изменение цены на сообщение со ссылкой в зависимости от делегаторства
                if check_for_delegator(i['from']):
                    price_for_linked_messages = config.price_for_delegator_message
                else:
                    price_for_linked_messages = config.price_for_linked_messages

                message_info = ''
                # если сообщение со ссылкой и сумма соответствует
                if check_for_link(payload) and value >= price_for_linked_messages:
                    message_info = bot.send_message(channgel_name, message_text, parse_mode='HTML',
                                                    disable_web_page_preview=True)  # отправка сообщения и сохранение его параметров
                    insert_into_transactions('Mt' + i['hash'], i['from'], coin, value, payload,
                                             'PUBLISHED')  # вставка в таблицу transactions со статусом PUBLISHED
                # если сообщение со ссылкой и сумма НЕ соотвествует
                elif check_for_link(payload) and value < price_for_linked_messages:
                    insert_into_transactions('Mt' + i['hash'], i['from'], coin, value, payload,
                                             'NOT PUBLISHED')  # вставка в таблицу transactions со статусом NOT PUBLISHED
                # если сообщение без ссылки и сумма соответствует
                elif not check_for_link(payload) and value >= price_for_linked_messages:
                    message_info = bot.send_message(channgel_name, message_text, parse_mode='HTML',
                                                    disable_web_page_preview=True)  # отправка сообщения и сохранение его параметров
                    insert_into_transactions('Mt' + i['hash'], i['from'], coin, value, payload,
                                             'PUBLISHED')  # вставка в таблицу transactions со статусом PUBLISHED
                # если сообщение без ссылки и сумма соответствует
                elif not check_for_link(
                        payload) and price_for_linked_messages > value >= config.price_for_ordinary_message:
                    message_info = bot.send_message(channgel_name, message_text, parse_mode='HTML',
                                                    disable_web_page_preview=True)  # отправка сообщения и сохранение его параметров
                    insert_into_transactions('Mt' + i['hash'], i['from'], coin, value, payload,
                                             'PUBLISHED')  # вставка в таблицу transactions со статусом PUBLISHED

                # если сумма соответствует сумме для закрепления на час, но не соответствует сумме для закрепления на день
                if config.price_for_pin_hour <= value < config.price_for_pin_day:
                    pin_message('hour', message_info)
                # если сумма соответсвует сумме для закрепления на день
                elif value >= config.price_for_pin_day:
                    pin_message('day', message_info)
            else:
                insert_into_transactions('Mt' + i['hash'], i['from'], coin, value, payload,
                                         'NOT PUBLISHED')  # вставка в таблицу transactions со статусом NOT PUBLISHED

    txns = txns2  # список старых транзакций заменяется на новые
    time.sleep(2)  # задержка на 2 секунды
